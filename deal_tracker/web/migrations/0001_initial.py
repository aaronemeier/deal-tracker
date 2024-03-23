from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import regex_field.fields

# pylint: skip-file
# flake8: noqa


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("url", models.URLField(max_length=1000, unique=True)),
                ("image_url", models.URLField(blank=True, max_length=1000)),
                ("name", models.CharField(blank=True, max_length=200)),
                ("description", models.CharField(blank=True, max_length=1000)),
                ("brand", models.CharField(blank=True, max_length=50)),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
                "db_table": "item",
            },
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("url", models.URLField(max_length=1000, unique=True)),
                ("domain", models.URLField(unique=True)),
                ("regex", regex_field.fields.RegexField(max_length=200, unique=True)),
                ("example", models.URLField(max_length=1000)),
                (
                    "currency",
                    models.CharField(
                        choices=[("CHF", "Swiss francs"), ("USD", "US Dollars")], default="CHF", max_length=10
                    ),
                ),
            ],
            options={
                "verbose_name": "Shop",
                "verbose_name_plural": "Shops",
                "db_table": "shop",
            },
        ),
        migrations.CreateModel(
            name="UserPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "language",
                    models.CharField(choices=[("en", "English"), ("de", "German")], default="en", max_length=2),
                ),
                (
                    "theme",
                    models.CharField(choices=[("LIGHT", "Light"), ("DARK", "Dark")], default="LIGHT", max_length=10),
                ),
                ("enable_list_view", models.BooleanField(blank=True, default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "User Preference",
                "verbose_name_plural": "User Preferences",
                "db_table": "user_preference",
            },
        ),
        migrations.CreateModel(
            name="PriceLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                ("price", models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30)),
                ("stock", models.IntegerField(blank=True, default=None, null=True)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="web.item")),
            ],
            options={
                "verbose_name": "Price Log",
                "verbose_name_plural": "Price Logs",
                "db_table": "price_log",
            },
        ),
        migrations.AddField(
            model_name="item",
            name="shop",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="web.shop"),
        ),
        migrations.CreateModel(
            name="Wish",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price_trigger", models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="web.item")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Wish",
                "verbose_name_plural": "Wishes",
                "db_table": "wish",
                "unique_together": {("item", "user")},
            },
        ),
        migrations.CreateModel(
            name="ShopPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("enabled", models.BooleanField(default=True)),
                ("discount", models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4)),
                ("shop", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="web.shop")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Shop Preference",
                "verbose_name_plural": "Shop Preferences",
                "db_table": "shop_preference",
                "unique_together": {("user", "shop")},
            },
        ),
    ]
