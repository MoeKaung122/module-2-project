from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib import messages
from hotel import models
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):

    hotel = models.Hotel.objects.all().order_by("id")

    search = request.GET.get("search")
    city = request.GET.get("city")

    if search:
        hotel = hotel.filter(name__icontains=search)

    if city and city.isdigit():
        hotel = hotel.filter(city_id=city)

    # PAGINATION
    paginator = Paginator(hotel, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "city": models.City.objects.all(),
        "old_search": search,
        "old_city": city,
    }

    return render(request, "index.html", context)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # hash password
            user.save()

            login(request, user)  # auto login after register
            return redirect("/")  # change to your homepage

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def Logout(request):
    logout(request)
    return redirect("/login/")


def Login(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect("/")
        else:
            messages.error(request, "Login Failed")
            return redirect("/login/")

@login_required(login_url="/login/")
def Hotel_Detail(request, id):
    hotel = models.Hotel.objects.get(id=id)
    room_types = models.RoomType.objects.filter(hotel_id=hotel.id)

    if request.method == "GET":
        return render(
            request, "hotel_detail.html", {"hotel": hotel, "room_type": room_types}
        )

    if request.method == "POST":
        room_type_id = request.POST.get("room_type")
        user = request.user
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        guests = request.POST.get("guests")
        # validate room type
        room_type = get_object_or_404(models.RoomType, id=room_type_id)

        room = models.Room.objects.filter(RoomType=room_type, is_available=True).first()
        if not room:
            messages.error(request, "No rooms available for this type.")

        d1 = datetime.strptime(check_in, "%Y-%m-%d").date()
        d2 = datetime.strptime(check_out, "%Y-%m-%d").date()
        nights = (d2 - d1).days
        # calculate total price
        total_price = room_type.base_price * nights

        Booking = models.Booking.objects.create(
            user=user,
            hotel=hotel,
            room_type=room_type,
            room=room,
            check_in=d1,
            check_out=d2,
            guests=guests,
            total_price=total_price,
        )

        # Update room availability
        room.is_available = False
        room.save()
        Booking.save()
        messages.success(request, "booking success")

        return redirect("/")  # your success page

@login_required(login_url="/login/")
def my_bookings(request):

    bookings = models.Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "booking.html", {"booking": bookings})

@login_required(login_url="/login/")
def booking_payment(request, id):
    booking = get_object_or_404(models.Booking, id=id, user=request.user)

    if request.method == "POST":
        method = request.POST.get("method")

        if not method:
            messages.error(request, "method fail")
        # Create a payment record
        models.Payment.objects.create(booking=booking, method=method)

        # Update only payment_status
        booking.payment_status = "paid"
        booking.save()

        return redirect("my_bookings")

    return render(request, "payment.html", {"booking": booking})


def about_us(request):
    return render(request, "about.html")


@login_required(login_url="/login/")
def blog(request):
    blog_posts = models.Blog.objects.all().order_by("-id")
    paginator = Paginator(blog_posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog.html" , {"page_obj": page_obj})


@login_required(login_url="/login/")
def blog_detail(request, id):
    blog_post = get_object_or_404(models.Blog, id=id)
    comments = models.Comment.objects.filter(blog=blog_post).order_by("-created_at")
    if request.method == "GET":
       return render(request, "blog_detail.html", {"blog": blog_post, "comments": comments})

    if request.method == "POST":
        content = request.POST.get("text")
        if content:
            models.Comment.objects.create(
                blog=blog_post,
                user=request.user,
                content=content
            )
            messages.success(request, "Comment created successfully")
            return redirect(f"/blog/detail/{blog_post.id}/#comment-box")
        
        
@login_required(login_url="/login/")
def toggle_like(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)   # Unlike
    else:
        blog.likes.add(request.user)      # Like

    return redirect(request.META.get("HTTP_REFERER", "/"))


def contact_us(request):

    if request.method == "GET":
        return render(request, "contact.html")
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            models.Contact.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, "Message sent successfully")
            return redirect("/contact/")