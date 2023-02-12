# Generated by Django 4.1.6 on 2023-02-12 12:16

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("title", models.CharField(max_length=50, verbose_name="title")),
                ("slug", models.SlugField(verbose_name="slug")),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
            },
        ),
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
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="store.brand",
                        verbose_name="brand",
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categories",
                "unique_together": {("slug", "parent")},
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("status", models.BooleanField(verbose_name="prouct status")),
                ("liked", models.IntegerField(verbose_name="number of liking")),
                ("price", models.FloatField(verbose_name="price")),
                ("discountPrice", models.FloatField(verbose_name="discount price")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                ("img", models.ImageField(upload_to="", verbose_name="image")),
                ("alt", models.CharField(max_length=50, verbose_name="image alt")),
                ("is_main", models.BooleanField(verbose_name="is the main img")),
            ],
            options={
                "verbose_name_plural": "ProductImages",
            },
        ),
        migrations.CreateModel(
            name="ProductOption",
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
                ("name", models.CharField(max_length=50, verbose_name="option name")),
            ],
        ),
        migrations.CreateModel(
            name="ProductOptionValues",
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
                ("value", models.CharField(max_length=50, verbose_name="value")),
                (
                    "related_img",
                    models.ImageField(upload_to="", verbose_name="option related img"),
                ),
                ("status", models.BooleanField(verbose_name="option status")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.product",
                        verbose_name="",
                    ),
                ),
                (
                    "productOption",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.productoption",
                        verbose_name="Product Option",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="img",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="store.productimage",
                verbose_name="Product Images",
            ),
        ),
        migrations.CreateModel(
            name="CardItem",
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
                ("quantity", models.IntegerField(verbose_name="quantity")),
                ("amount", models.FloatField(verbose_name="amount")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.product",
                        verbose_name="product ordered",
                    ),
                ),
            ],
            options={
                "verbose_name": "CardItem",
                "verbose_name_plural": "CardItems",
            },
        ),
        migrations.CreateModel(
            name="Card",
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
                ("totale", models.FloatField(verbose_name="totale")),
                (
                    "CardItem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.carditem",
                        verbose_name="Card Items",
                    ),
                ),
            ],
            options={
                "verbose_name": "Card",
                "verbose_name_plural": "Cards",
            },
        ),
    ]
