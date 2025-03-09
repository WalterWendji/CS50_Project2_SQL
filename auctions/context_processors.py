from .models import Watchlist

def global_settings(request):
    length_of_watchlist = ""
    if request.user.is_authenticated:
        length_of_watchlist = Watchlist.objects.filter(user=request.user).count() 
    return {
        "length_of_watchlist": length_of_watchlist
    }
