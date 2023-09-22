from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Название товара"))
    price = models.PositiveIntegerField(verbose_name=_("Цена товара"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Описание товара"))
    availability = models.BooleanField(default=True, verbose_name=_("Наличие товара"))
    club = models.ForeignKey('tickets.Club', on_delete=models.CASCADE, verbose_name=_("Клуб"))
    slug = models.SlugField(max_length=30, unique=True, db_index=True, verbose_name="URL")
    option_values = models.ManyToManyField('OptionValue', blank=False, through='ProductOption', verbose_name=_("Опции"))
    categories = models.ManyToManyField('Category', blank=True, verbose_name=_("Категории"))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'product_slug': self.slug})

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(categories__pk=category_id)
        else:
            return Product.get_all_products()

    # @property
    def all_products_without_instance_by_categoryid(self, category_id):
        if category_id:
            return Product.objects.filter(categories__pk=category_id).exclude(pk=self.pk)
        else:
            return Product.get_all_products()

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        ordering = ['name']


class ProductOption(models.Model):
    option_value = models.ForeignKey('OptionValue', on_delete=models.CASCADE, verbose_name=_("Значение опции"))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_("Товар"))
    count_product = models.PositiveIntegerField(verbose_name=_("Количество товара с данной опцией"), default=0)

    class Meta:
        verbose_name = _('Опция, связанная с товаром')
        verbose_name_plural = _('Опции, связанные с товаром')
        unique_together = ('option_value', 'product',)


class OptionValue(models.Model):
    option = models.ForeignKey('Option', on_delete=models.PROTECT, verbose_name=_("Опция"))
    value = models.CharField(max_length=20, verbose_name=_("Вариант опции"))

    def __str__(self):
        return f"{self.option}: {self.value}"

    class Meta:
        verbose_name = _('Значение опции')
        verbose_name_plural = _('Значения опций товаров')
        ordering = ['option']
        unique_together = ('option', 'value',)


class Option(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Название опции"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Опция товара')
        verbose_name_plural = _('Опции товаров')
        ordering = ['name']


class ProductPhoto(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_("Товар"))
    photo = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name=_("Фотография"))

    class Meta:
        verbose_name = _('Фотография товара')
        verbose_name_plural = _('Фотографии товаров')
        ordering = ['pk']


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Название категории"))
    slug = models.SlugField(max_length=30, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория товара')
        verbose_name_plural = _('Категории товаров')
        ordering = ['name']


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CRE', _('Создан')
        PAID = 'PAI', _('Оплачен')
        COLLECT = 'COL', _('В сборке')
        DELIVERY = 'DEL', _('В доставке')
        CAN_PICK_IT_UP = 'PIC', _('Готов к выдаче')
        RECEIVED = 'REC', _('Получен')
        CANCEL = 'CAN', _('Отменён')

    customer = models.ForeignKey('userapp.User', on_delete=models.PROTECT, null=True, verbose_name=_("Покупатель"))
    email = models.EmailField(unique=False, verbose_name=_("Эл. почта"))
    phone_number = models.CharField(null=False, max_length=16, unique=False, verbose_name=_("Номер телефона"))
    status = models.CharField(max_length=3, verbose_name=_("Статус заказа"),
                              choices=Status.choices, default=Status.CREATED)
    shipping_address = models.CharField(max_length=500, verbose_name=_("Адрес доставки"))
    cost_order = models.PositiveIntegerField(verbose_name=_("Стоимость заказа"))
    details = models.ManyToManyField('ProductOption', through='OrderDetails')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения статуса")

    def __str__(self):
        return f"{self.pk} - {self.shipping_address}, стоимость {self.cost_order}"

    def get_absolute_url(self):
        return reverse('shop:order', kwargs={'order_slug': self.pk})

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['time_create']


class OrderDetails(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name=_("Заказ"))
    product = models.ForeignKey('ProductOption', on_delete=models.CASCADE, verbose_name=_("Товар"))
    quantity = models.PositiveIntegerField(verbose_name=_("Количество товара"))
    sum_product = models.PositiveIntegerField(verbose_name=_("Сумма за товар"))

    class Meta:
        verbose_name = _('Детали заказа')
        verbose_name_plural = _('Детали заказов')
        ordering = ['order']
