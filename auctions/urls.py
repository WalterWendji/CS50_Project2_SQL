from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_new_listing, name="newListing"),
    path("listings/<int:auction_id>", views.listing, name="listing"),
    path("watchlist", views.show_watchlist, name="watchlist")
]
