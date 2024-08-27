from django.urls import path
from . import views

app_name='core'

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<str:pk>/', views.property_detail, name='property'),
    path('properties/', views.all_properties, name='properties'),
    path('favourite/<str:pk>/', views.favorite, name='add_favourite'),
    path('remove-favourite/<str:pk>/', views.remove_favourite, name='remove_favourite'),
    path('create-property/', views.create_property, name='create_property'),
    # path('<slug:slug>/', views.home, name='category'),
]
