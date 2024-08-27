from django.contrib import admin
from . models import Category, Property, Amenity, PropertyAmenity, Booking, Review, AddFavorite

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Amenity)
admin.site.register(PropertyAmenity)
admin.site.register(AddFavorite)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_per_night', 'city', 'country', 'guests', 'check_in_time', 'check_out_time', 'is_available']
    list_editable = ['price_per_night',  'country', 'guests', 'check_in_time', 'check_out_time', 'is_available']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):   
    list_display = ['property', 'guest', 'check_in_date', 'check_out_date', 'guests', 'created_at', 'updated_at']