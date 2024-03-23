import logging

from captcha.fields import ReCaptchaField
from django import forms
from django.utils.translation import gettext as _
from django_registration.forms import RegistrationFormUniqueEmail

from .models import UserPreference, Shop, Wish
from .utils import get_domain_from_url

LOG = logging.getLogger(__name__)


class RegistrationForm(RegistrationFormUniqueEmail):
    captcha = ReCaptchaField(label="I'm a human")


class WishCreateForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ["url", "price_trigger"]

    url = forms.URLField(label=_("Product URL"), help_text=_("Enter a product url as a reference for the product"))

    price_trigger = forms.DecimalField(
        label=_("Price trigger"),
        required=False,
        help_text=_(
            "Select a price trigger, on which email notifications will be sent. Use zero to disable the price trigger."
        ),
        initial=0.0,
    )

    def clean_url(self):
        form_data = self.cleaned_data
        if form_data["url"]:
            url = form_data["url"]
            domain = get_domain_from_url(url)

            try:
                shop = Shop.objects.get(domain=domain)
                if not shop.regex.match(url):
                    self.add_error("url", _(f"Specified URL is invalid. Example: {shop.example}"))

                else:
                    form_data["shop"] = shop.id

            except (Shop.DoesNotExist, ValueError):
                self.add_error("url", _("No shop support for specified url"))

            return url
        return None


class WishUpdateForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = ["price_trigger"]

    price_trigger = forms.DecimalField(label=_("Update Price trigger"), required=False)


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ["language", "theme"]

    language = forms.ChoiceField(label=_("Language"), choices=UserPreference.language_choices)
    theme = forms.ChoiceField(label=_("Theme"), choices=UserPreference.theme_choices)
    enable_list_view = forms.BooleanField(label=_("Enable list view "), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for shop in Shop.objects.all():
            self.fields[f"shop_enabled_{shop.id}"] = forms.BooleanField(
                label=_(f"Enable emails for {shop.name}"), required=False, initial=True
            )
            self.fields[f"shop_discount_{shop.id}"] = forms.DecimalField(
                label=_(f"Discount (in %) for {shop.name}"), required=False, initial=0.0, decimal_places=2
            )

    def _clean_fields(self):
        super()._clean_fields()
        for shop in Shop.objects.all():
            # discount = self.fields[f'shop_discount_{shop.id}']
            discount = self.cleaned_data[f"shop_discount_{shop.id}"]
            if discount >= 100:
                self.add_error(f"shop_discount_{shop.id}", _("Discount can't be higher than 100% "))
                LOG.error(self.errors)
            if discount < 0:
                self.add_error(f"shop_discount_{shop.id}", _("Discount can't be less than 0% "))


class WorkerAdministrationForm(forms.Form):
    ACTIONS = (
        ("scrape_all", _("Scrape all items")),
        ("send_mail", _("Send all mails")),
    )

    action = forms.ChoiceField(choices=ACTIONS)
