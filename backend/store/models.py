from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext as _
from django.utils.text import slugify
from account.models import User

class Brand(models.Model):
    title = models.CharField(_("title"), max_length=50)
    slug = models.SlugField(_("slug"),unique=True)
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Brand,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug
    @staticmethod
    def get_all_brands():
        return Brand.objects.all()

class Category(MPTTModel):
    """ category with sub categories """
    name   = models.CharField(max_length=200)
    slug   = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )
    brand  = models.ManyToManyField(
        Brand, 
        related_name="products", 
        verbose_name=_("brand"), 
    )

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    

class ProductImage(models.Model):
    img = models.CharField(_("image"), max_length=254)
    alt = models.CharField(_("image alt"), max_length=50)

    def __str__(self) -> str:
        return self.alt

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images") 

class ProductOption(models.Model):
    name = models.CharField(_("option name"), max_length=50)
    def __str__(self):
        return self.name

class ProductOptionValues(models.Model):
    productOption = models.ForeignKey(ProductOption, verbose_name=_("Product Option"), on_delete=models.CASCADE)
    value = models.CharField(_("value"), max_length=50)
    related_img = models.ForeignKey(ProductImage, verbose_name=_("product option image "), on_delete=models.CASCADE)
    status = models.BooleanField(_("option status"))

class Product(models.Model):
    """ product model """
    mainImg     = models.CharField(verbose_name="main image", max_length=255)
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(unique=True)
    imgs         = models.ManyToManyField(
        ProductImage, 
        related_name=_("products"), 
        verbose_name=_("Product Images"),
        null=True
    )
    description = models.TextField(blank=True,null=True)
    category    = models.ManyToManyField(
        Category,
        related_name=_("products"),
        verbose_name=_("catgories")
    )
    productOptionValues = models.ManyToManyField(
        ProductOptionValues,
        related_name=_("products"),
        verbose_name=_("product option values"),
        null=True
    )
    status = models.BooleanField(_("prouct status"),blank=True,null=True)
    liked = models.IntegerField(_("number of liking"),blank=True,null=True)
    price = models.FloatField(_("price"))
    discountPrice = models.FloatField(_("discount price"),blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    @staticmethod
    def get_products_by_slug(slug):
        return Product.objects.get(slug=slug)
  
    @staticmethod
    def get_all_products():
        return Product.objects.all()
  
    @staticmethod
    def get_products_by_category(category):
        if category:
            return Product.objects.filter(category=category)
        else:
            return Product.get_all_products()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

class CardItem(models.Model):

    product  = models.ForeignKey(Product, verbose_name=_("product ordered"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"))
    amount   = models.FloatField(_("amount"),blank=True,null=True)

    class Meta:
        verbose_name = _("CardItem")
        verbose_name_plural = _("CardItems")

    def save(self, *args, **kwargs):
        if not self.product.discountPrice:
            self.amount = self.quantity * self.product.price
        else:
            self.amount = self.quantity * self.product.discountPrice
        super(CardItem,self).save(*args, **kwargs)

class Card(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_("user card"), on_delete=models.CASCADE)
    cardItems = models.ManyToManyField(CardItem, verbose_name=_("Card Items"))
    totale = models.FloatField(_("totale"),blank=True,null=True)

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def save(self, *args, **kwargs):
        for item in self.cardItems:
            self.totale += item.amount
            
        super(Card,self).save(*args, **kwargs)

class Shipping(models.Model):
    card = models.ForeignKey(Card, verbose_name=_("card"), on_delete=models.CASCADE)
    address = models.CharField(_("shipping address"), max_length=250)
    phone = models.IntegerField(_("phone numbere"))
    totalePayed = models.FloatField(_("totale payed"))
    status = models.BooleanField(_("shipping status"))
    payementValiation = models.BooleanField(_("payement validation"))
    phippingCost = models.FloatField(_("Shipping cost"))

    class Meta:
        verbose_name = _("shipping")
        verbose_name_plural = _("Shippings")
