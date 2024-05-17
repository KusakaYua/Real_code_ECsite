# Generated by Django 5.0.4 on 2024-04-30 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core_page", "0003_cartitem_quantity_alter_cartitem_item"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "商品カテゴリ",
                "verbose_name_plural": "商品カテゴリ",
            },
        ),
        migrations.AlterModelOptions(
            name="cart",
            options={"verbose_name": "カート", "verbose_name_plural": "カート"},
        ),
        migrations.AlterModelOptions(
            name="cartitem",
            options={"verbose_name": "カートアイテム", "verbose_name_plural": "カートアイテム"},
        ),
        migrations.AlterModelOptions(
            name="item",
            options={"verbose_name": "商品", "verbose_name_plural": "商品"},
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "注文", "verbose_name_plural": "注文"},
        ),
        migrations.AddField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="core_page.category",
            ),
        ),
    ]