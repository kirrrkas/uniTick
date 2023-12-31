# Generated by Django 4.1.7 on 2023-05-15 19:15

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Эл. почта')),
                ('phone_number', models.CharField(max_length=16, verbose_name='Номер телефона')),
                ('status', models.CharField(choices=[('CRE', 'Создан'), ('PAI', 'Оплачен'), ('COL', 'Собран'), ('DEL', 'В доставке'), ('PIC', 'Готов к выдаче'), ('REC', 'Получен')], max_length=3, verbose_name='Статус заказа')),
                ('shipping_address', models.CharField(max_length=500, verbose_name='Адрес доставки')),
                ('cost_order', models.PositiveIntegerField(verbose_name='Стоимость заказа')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения статуса')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['time_create'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('price', models.PositiveIntegerField(verbose_name='Цена товара')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('availability', models.BooleanField(default=True, verbose_name='Наличие товара')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='URL')),
                ('categories', models.ManyToManyField(blank=True, to='shop.category', verbose_name='Категории')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.club', verbose_name='Клуб')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название опции')),
                ('variants', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, size=None, verbose_name='Варианты опции')),
            ],
            options={
                'verbose_name': 'Опция товара',
                'verbose_name_plural': 'Опции товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Фотография')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фотография товара',
                'verbose_name_plural': 'Фотографии товаров',
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='options',
            field=models.ManyToManyField(blank=True, to='shop.productoption', verbose_name='Опции'),
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество товара')),
                ('sum_product', models.PositiveIntegerField(verbose_name='Сумма за товар')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказов',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='details',
            field=models.ManyToManyField(through='shop.OrderDetails', to='shop.product'),
        ),
    ]
