import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, FormView

from . import tasks
from .constants import CeleryQueues
from .forms import PreferencesForm, WishUpdateForm, WishCreateForm, WorkerAdministrationForm
from .models import Wish, Shop, UserPreference, ShopPreference, Item
from .services import get_items_for_user, get_wish_info, get_preference, get_price_log_infos

LOG = logging.getLogger(__name__)

UserModel = get_user_model()


class WishListView(LoginRequiredMixin, ListView):
    template_name_field = "wish"
    template_name_suffix = "_album"

    def __init__(self, *args, **kwargs):
        self.object_list = None
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object_list = get_items_for_user(self.request.user)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_template_names(self):
        user = self.request.user
        preference = get_preference(user)
        if preference is not None and preference["enable_list_view"]:
            self.template_name_suffix = "_list"
        return f"web/{self.template_name_field}{self.template_name_suffix}.html"


class WishDetailView(LoginRequiredMixin, UpdateView):
    template_name = "web/wish_detail.html"
    model = Wish
    form_class = WishUpdateForm

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        info = get_wish_info(user, self.object.id)
        if info is None:
            raise Http404(_("Wish information not found or it is currently refreshing with the latest price data"))

        context["info"] = info
        context["price_log"] = get_price_log_infos(info["item"].id)
        if context["price_log"] is None:
            raise Http404(_("Price update information not found"))
        return context

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Wish, id=self.kwargs["pk"], user=request.user)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return self.request.path


class WishCreateView(LoginRequiredMixin, CreateView):
    template_name = "web/wish_form.html"
    form_class = WishCreateForm
    success_url = reverse_lazy("wish_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shops"] = ", ".join(shop.name for shop in Shop.objects.all())
        return context

    def form_valid(self, form):
        user = self.request.user
        url = form.cleaned_data["url"]
        price_trigger = form.cleaned_data["price_trigger"]
        shop = Shop.objects.get(id=form.cleaned_data["shop"])

        item, _ = Item.objects.update_or_create(url=url, defaults={"shop": shop})
        item.save()
        tasks.scrape_item.s(item_id=item.id).apply_async(queue=CeleryQueues.HIGH_PRIORITY)

        wish, _ = Wish.objects.update_or_create(item=item, user=user, defaults={"price_trigger": price_trigger})
        wish.save()

        return HttpResponseRedirect(self.success_url)


class WishDeleteView(LoginRequiredMixin, DeleteView):  # type: ignore
    template_name_field = "wish"
    success_url = "/"
    model = Wish

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_queryset().filter(pk=kwargs.get("pk"))
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class PreferencesUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "web/preferences_form.html"
    form_class = PreferencesForm
    success_url = reverse_lazy("preferences")

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        preference = get_preference(user)
        if preference is not None:
            self.initial = preference
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = PreferencesForm(request.POST)
        if form.is_valid():
            user = request.user
            preference, _ = UserPreference.objects.update_or_create(
                user=user,
                defaults={
                    "language": form.cleaned_data.get("language"),
                    "theme": form.cleaned_data.get("theme"),
                    "enable_list_view": form.cleaned_data.get("enable_list_view"),
                },
            )
            preference.save()

            for shop in Shop.objects.all():
                enabled = bool(form.cleaned_data.get(f"shop_enabled_{shop.id}"))
                discount = form.cleaned_data.get(f"shop_discount_{shop.id}")

                preference, _ = ShopPreference.objects.update_or_create(
                    user=user, shop=shop, defaults={"enabled": enabled, "discount": discount}
                )
                preference.save()
            return HttpResponseRedirect(self.success_url)
        return self.get(request, *args, **kwargs)


class UserDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):  # type: ignore
    template_name = "web/user_delete_form.html"
    success_url = reverse_lazy("wish_list")

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        success_url = self.get_success_url()
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        if self.request.user:
            user = self.request.user
            return not user.is_superuser
        return False


class WorkerAdministrationView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "web/worker.html"
    permission_required = "is_superuser"
    form_class = WorkerAdministrationForm
    success_url = reverse_lazy("preferences_worker")

    def form_valid(self, form):
        context = self.get_context_data()
        action = form.cleaned_data["action"]
        notification = {"message": _("Unknown action"), "type": "error"}

        if action == "scrape_all":
            tasks.scrape_tracked_items.s().apply_async()
            notification["message"] = _("Job submitted: Scraping all items")
            notification["type"] = "success"

        if action == "send_mail":
            tasks.send_mails.s().apply_async()
            notification["message"] = _("Job submitted: Sending mails")
            notification["type"] = "success"

        context["notification"] = notification
        return self.render_to_response(context)
