from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Myanmar")
    image = models.ImageField(upload_to="city_images/", null=True, blank=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="hotels")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()

    star = models.PositiveSmallIntegerField(default=3)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    phone = models.CharField(max_length=20, default="Unknown")
    email = models.EmailField(blank=True, null=True)

    lowest_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="hotels/", blank=True, null=True)

    # Auto fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="room_types"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    max_guests = models.PositiveIntegerField(default=2)
    beds = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(help_text="Room size in sq ft", default=200)

    image = models.ImageField(upload_to="room_types/", blank=True, null=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Room(models.Model):
    RoomType = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="room"
    )
    room_number = models.CharField(max_length=50)
    floor = models.PositiveBigIntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} {self.RoomType}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    check_in = models.DateField()
    check_out = models.DateField()

    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status_choices = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS = (
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="unpaid")

    status = models.CharField(max_length=20, choices=status_choices, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel.name}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20)  
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)  # admin approval optional

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name