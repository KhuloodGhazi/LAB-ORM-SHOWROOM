from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Brand
from cars.models import Car
from django.contrib import messages
from django.db.models import Count




# Create your views here.

def all_brands_view(request:HttpRequest):
    
    search_query = request.GET.get('search', '')  
    
    brands = Brand.objects.annotate(car_count=Count('cars')).filter(
        brand_name__icontains=search_query) if search_query else Brand.objects.annotate(car_count=Count('cars'))

    return render(request, 'brands/all_brands.html', {'brands': brands, 'search_query': search_query})



def add_new_brand_view(request:HttpRequest):

    if not request.user.is_superuser:
        messages.error(request, "Only admin can add brand")

        return redirect("main:main_view")
    
    if request.method == "POST":
        new_brand = Brand(
            brand_name=request.POST["brand_name"],
            about=request.POST["about"],
            logo=request.FILES["logo"],
            country_of_origin=request.POST["country_of_origin"],
            founded_at=request.POST["founded_at"],
            )

        new_brand.save()

        messages.success(request, "Brand successfully added!")

        return redirect("brands:brand_details_view", brand_id=new_brand.id)
    
    return render(request, 'brands/add_new_brand.html')




def brand_details_view(request:HttpRequest, brand_id):

    brand = get_object_or_404(Brand, id=brand_id)
    cars = brand.cars.all()

    return render(request, 'brands/brand_details.html', {"brand": brand, "cars": cars})




def brand_update_view(request:HttpRequest, brand_id):

    brand = get_object_or_404(Brand, pk=brand_id)

    if not request.user.is_superuser:
        messages.error(request, "Only admin can update brand")

        return redirect("main:main_view")

    if request.method == "POST":
        brand.brand_name=request.POST.get("brand_name", brand.brand_name)
        brand.about=request.POST.get("about", brand.about)
        brand.founded_at=request.POST.get("founded_at", brand.founded_at)
        brand.country_of_origin=request.POST.get("country_of_origin", brand.country_of_origin)

        if request.FILES.get("logo"):
            brand.logo=request.FILES["logo"]

        brand.save()    
        messages.success(request, "Brand Updated successfully!")


        return redirect("brands:brand_details_view", brand_id=brand.id)

    return render(request, 'brands/update_brand.html', {"brand": brand})




def brand_delete_view(request:HttpRequest, brand_id):
    
    brand = get_object_or_404(Brand, pk=brand_id)

    if not request.user.is_superuser:
        messages.error(request, "Only admin can delete brand")

        return redirect("main:main_view")
    
    brand.delete()

    messages.success(request, "Brand deleted successfully!")

    return redirect('main:main_view')


