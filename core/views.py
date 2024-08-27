from django.shortcuts import render, get_object_or_404, redirect
from core.models import Category, Property, AddFavorite
from core.filters import PropertyFilter, ListFilter
from django.contrib import messages
from django_countries import countries
from .forms import PropertyForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    property_filter = PropertyFilter(request.GET, queryset=Property.objects.all().order_by('-created_at'))  # Order by a specific field
    paginator = Paginator(property_filter.qs, 3)  # Pass the ordered queryset to Paginator
    page_number = request.GET.get('page')
    categories = Category.objects.all()
    
    try:
        properties = paginator.page(page_number)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)
    
    template_name = 'core/home.html'
    if request.htmx:
        template_name = 'core/snippets/property_list.html'
    
    context = {
        'properties': properties,
        'categories': categories,
    }
    
    return render(request, template_name, context)

@login_required
def favorite(request, pk):
    favorite = get_object_or_404(Property, pk=pk)
    user = request.user
    AddFavorite.objects.get_or_create(user=user, property=favorite)
    messages.info(request, f'You add {favorite.title} to your have Favorite')
    return redirect('core:home')
@login_required
def remove_favourite(request, pk):
    favorite = get_object_or_404(pk=pk)
    user = request.user
    AddFavorite.objects.filter(user=user, property=favorite).delete()
    messages.warning(request, f"You have removed {favorite.title} from your favorites")
    return redirect('core:home')

def all_properties(request):
    property_filter = ListFilter(request.GET, queryset=Property.objects.all())
    categories = Category.objects.all()
    context = {'properties': property_filter.qs, 'categories':categories}
    template_name = 'core/properties.html'
    if request.htmx:
        template_name = 'core/snippets/property_list.html'
    return render(request, template_name, context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property
    }
    return render(request, 'core/property.html', context)


def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            if Property.objects.filter(title=title).exists():
                messages.warning(request, 'Property with this title already exists')
            else:
                prop = form.save(commit=False)
                prop.owner = request.user
                prop.save()
                messages.success(request, 'Property Created Successfully')
                return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = PropertyForm()
    context = {
        'countries': countries,
        'form': form,
    }
    return render(request, 'core/create_property.html', context)
