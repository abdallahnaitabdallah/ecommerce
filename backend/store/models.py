from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext as _
import slugify



class Brand(models.Model):
    title = models.CharField(_("title"), max_length=50)
    slug = models.SlugField(_("slug"))
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.slug

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
    brand  = models.ForeignKey(
        Brand, 
        related_name="products", 
        verbose_name=_("brand"), 
        on_delete=models.CASCADE
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

class ProductImage(models.Model):
    img = models.CharField(_("image"), max_length=254)
    alt = models.CharField(_("image alt"), max_length=50)
    is_main = models.BooleanField(_("is the main img"))
    def __str__(self) -> str:
        return self.alt

    class Meta:
        verbose_name_plural = "ProductImages" 

class Product(models.Model):
    """ product model """
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(unique=True)
    img         = models.ForeignKey(
        ProductImage, 
        related_name="products", 
        verbose_name=_("Product Images"), 
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True,null=True)
    category    = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

class ProductOption(models.Model):
    name = models.CharField(_("option name"), max_length=50)
    def __str__(self):
        return self.name

class ProductOptionValues(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(""), on_delete=models.CASCADE)
    productOption = models.ForeignKey("ProductOption", verbose_name=_("Product Option"), on_delete=models.CASCADE)
    value = models.CharField(_("value"), max_length=50)
    related_img = models.ForeignKey(ProductImage, verbose_name=_("product option image "), on_delete=models.CASCADE)
    status = models.BooleanField(_("option status"))

    def __str__(self):
        return self.name

class CardItem(models.Model):
    product  = models.ForeignKey(Product, verbose_name=_("product ordered"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"))
    amount   = models.FloatField(_("amount"),)

    class Meta:
        verbose_name = _("CardItem")
        verbose_name_plural = _("CardItems")

    def save(self, *args, **kwargs):
        if not self.product.discountPrice:
            self.amount = self.quantity * self.product.price
        else:
            self.amount = self.quantity * self.product.discountPrice
        super(Product,self).save(*args, **kwargs)

class Card(models.Model):

    cardItems = models.ManyToManyField(CardItem, verbose_name=_("Card Items"), on_delete=models.CASCADE)
    totale = models.FloatField(_("totale"))

    class Meta:
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def save(self, *args, **kwargs):
        for item in self.cardItems:
            self.totale += item.amount
            
        super(Product,self).save(*args, **kwargs)