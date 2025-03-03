from django.urls import path
#from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    #path("login", auth_views.LoginView.as_view()),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_new_listing, name="newListing"),
    path("listings/<int:auction_id>", views.show_listing, name="listing"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("category", views.show_categories, name="category"),
    path("category/<str:category_name>", views.show_category_details, name="category_listing")
]
