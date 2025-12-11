from django.urls import path

from hotel import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="login_out"),
    path("hotel/detail/<int:id>/", views.Hotel_Detail),
    path("booking/", views.my_bookings, name="my_bookings"),
    path("about/", views.about_us, name="about"),
    path("payment/<int:id>/", views.booking_payment, name="payment"),
    path("blog/", views.blog, name="blog"),
    path("blog/detail/<int:id>/", views.blog_detail, name="blog_detail"),
    path('blog/<int:blog_id>/like/', views.toggle_like, name='blog_like'),
    path("contact/", views.contact_us, name="contact"),
]
