from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    phone = models.CharField(max_length=20, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return '{} {} - {}'.format(self.first_name, self.last_name, self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Color(models.Model):
    color_name = models.CharField(max_length=30)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.color_name = str(self.color_name).title()
        self.slug = slugify(self.color_name)
        super(Color, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.color_name)


class Size(models.Model):
    size_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.size_name)


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["category_name"]

    def __str__(self) -> str:
        if self.parent:
            return "{} {}".format(str(self.parent), str(self.category_name))

        return str(self.category_name)

    def save(self, *args, **kwargs):
        if not self.parent:
            self.slug = slugify(str(self.category_name))
        else:
            self.slug = slugify('{} {}'.format(
                str(self.parent), str(self.category_name)))
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='static/shop/images/')

    def __str__(self) -> str:
        return '{} - {}'.format(str(self.product_name), str(self.color.color_name))

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify('{} {} {}'.format(str(self.category.category_name),
                                              str(self.product_name),
                                              str(self.color)))
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Product, self).delete(*args, **kwargs)


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    def __str__(self) -> str:
        return '{} - {} - {}'.format(str(self.product.product_name), str(self.product.color.color_name), str(self.size))


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)

    @ property
    def get_total_price(self):
        return self.item.price * self.quantity

    def __str__(self) -> str:
        return '{} / {}'.format(str(self.user.email), str(self.item))


class Order(models.Model):
    STATUS_NAME = {
        ('Completed', 'Completed'),
        ('On Process', 'On Process'),
        ('On Delivery', 'On Delivery'),
        ('Refunded', 'Refunded'),
        ('Cancelled', 'Cancelled')
    }
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_item = models.ManyToManyField(OrderItem, related_name='orderitem')
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=STATUS_NAME, default='On Process')
    transaction_id = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self) -> str:
        return '{} - {}'.format(str(self.transaction_id), str(self.status))


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    recipient = models.CharField(max_length=100, null=True)
    recipient_phone = models.CharField(max_length=20, null=True)
    recipient_email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    country = CountryField(null=True)

    class Meta:
        verbose_name_plural = "Shipping Addresses"

    @ property
    def get_full_address(self):
        full_address = "{}, {}, {}, {}, {}".format(str(self.address), str(
            self.city), str(self.state), str(self.country), str(self.zipcode))
        return full_address
