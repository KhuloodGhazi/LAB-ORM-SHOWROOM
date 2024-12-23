from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Car, Color, Review
from brands.models import Brand
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q




# Create your views here.

def all_cars_view(request:HttpRequest):

    search_query = request.GET.get('search', '')  
    brand_filter = request.GET.get('brand', '')   
    color_filter = request.GET.get('color', '')  

    cars = Car.objects.all()

    if search_query:
        cars = cars.filter(
            Q(car_name__icontains=search_query) |
            Q(price__icontains=search_query)
        )

    if brand_filter:
        cars = cars.filter(brand_id=brand_filter)   

    
    if color_filter:
        cars = cars.filter(available_colors__id=color_filter)

    paginator = Paginator(cars, 6) 
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number) 

    brands = Brand.objects.all()
    colors = Color.objects.all()        

    return render(request, "cars/all_cars.html", {"cars": cars_page, "brands": brands, "colors": colors})




def add_new_car_view(request:HttpRequest):

    if not request.user.is_superuser:
        messages.error(request, "Only admin can add car")

        return redirect("main:main_view")

    if request.method == "POST":
        car_name = request.POST.get("car_name")
        brand_id = request.POST.get("brand")
        available_colors = request.POST.getlist("available_colors")
        year = request.POST.get("year")
        engine = request.POST.get("engine")
        power = request.POST.get("power")
        price = request.POST.get("price")
        availability = request.POST.get("availability")
        speed = request.POST.get("speed")
        image = request.FILES.get("image")

        brand = get_object_or_404(Brand, id=brand_id)
        
        car = Car.objects.create(
            car_name=car_name,
            brand=brand,
            year=year,
            engine=engine,
            power=power,
            price=price,
            availability=availability,
            speed=speed,
            image=image
            )

        for color_id in available_colors:
            color = Color.objects.get(id=color_id)
            car.available_colors.add(color)


        messages.success(request, "Car successfully added!")

        return redirect("cars:car_details_view", car_id=car.id)
    
    colors = Color.objects.all()
    brands = Brand.objects.all()


    return render(request, 'cars/add_new_car.html', {"colors": colors, "brands": brands})




def car_details_view(request:HttpRequest, car_id: int):
    
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all() 

    return render(request, "cars/car_details.html", {"car": car, "reviews": reviews})




def car_update_view(request:HttpRequest, car_id: int):
    
    car = get_object_or_404(Car, pk=car_id)

    if not request.user.is_superuser:
        messages.error(request, "Only admin can update car")
        return redirect("main:main_view")

    if request.method == "POST":
        car.car_name=request.POST.get("car_name", car.car_name)
        brand_id = request.POST.get("brand")
        if brand_id:
            car.brand = get_object_or_404(Brand, pk=brand_id)

        color_ids = request.POST.getlist("available_colors")
        car.available_colors.set(Color.objects.filter(id__in=color_ids))    

        car.year=request.POST.get("year", car.year)
        car.engine=request.POST.get("engine", car.engine)
        car.power=request.POST.get("power", car.power)
        car.price=request.POST.get("price", car.price)
        car.availability=request.POST.get("availability", car.availability)
        car.speed=request.POST.get("speed", car.speed)

        if request.FILES.get("image"):
            car.image=request.FILES["image"]

        car.save()    
        messages.success(request, "Car Updated successfully!")

        return redirect("cars:car_details_view", car_id=car.id)
    
    brands = Brand.objects.all()
    colors = Color.objects.all()

    return render(request, 'cars/update_car.html', {"car": car, "brands": brands, "colors": colors})




def car_delete_view(request:HttpRequest, car_id: int):
    
    car = get_object_or_404(Car, pk=car_id)
    
    if not request.user.is_superuser:
        messages.error(request, "Only admin can delete car")
        return redirect("main:main_view")
    
    car.delete()

    messages.success(request, "Car deleted successfully!")

    return redirect('main:main_view')




def add_new_color_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        hex_code = request.POST.get("hex_code")

        if name and hex_code:
            Color.objects.create(name=name, hex_code=hex_code)

            messages.success(request, "Color added successfully!")

            return redirect(request.GET.get("next", "/"))
        

        else:
            messages.error(request, "Please provide all required fields.")

    return render(request, 'cars/add_new_color.html')




def update_color_view(request, color_id):
    color = get_object_or_404(Color, id=color_id)

    if request.method == "POST":
        color.name = request.POST.get("name", color.name)
        color.hex_code = request.POST.get("hex_code", color.hex_code)

        color.save()

        messages.success(request, "Color updated successfully!")

        return redirect("cars:car_details_view")

    return render(request, 'cars/update_color.html', {"color": color})




def add_review_view(request, car_id):

    car = get_object_or_404(Car, pk=car_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(car=car, user=request.user, rating=rating, comment=comment)

        messages.success(request, "Your review has been added successfully!")

        return redirect("cars:car_details_view", car_id=car.id)

    return render(request, "cars/add_review.html", {"car": car})
