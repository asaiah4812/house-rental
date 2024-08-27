from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.templatetags.static import static
import uuid

class Category(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse("core:home", args=[self.slug])
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    country = CountryField(blank=True, null=True)
    image1 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='properties/images/', blank=True, null=True)
    category = models.ManyToManyField(Category)
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def propImg(self):
        try:
            propImg = self.image1.url
        except:
            propImg = static('images/defaultcard.jpg')
        return propImg

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:property", args=[self.pk])
    

    class Meta:
        verbose_name_plural = 'Properties'

class AddFavorite(models.Model):
    property = models.ForeignKey(Property, related_name='favorites', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.property.title)



class Amenity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Amenities'

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    def __str__(self):
        return self.property
    class Meta:
        verbose_name_plural = 'PropertyAmenities'

class Booking(models.Model):
    PRO_STA = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
        )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PRO_STA, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        total_days = (self.check_out_date - self.check_in_date).days
        total_price = total_days * self.property.price_per_night * self.guests
        return total_price

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super(Booking, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.guest.username}'s booking for {self.property.title}"

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username}'s review for {self.property.title}"