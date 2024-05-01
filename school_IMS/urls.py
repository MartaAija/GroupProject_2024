#     WORKED ON FILE:
#       - Emina Asherbekova (w1830501) 

from django.contrib import admin
from django.urls import path, include
from static_pages.views import home
from django.conf.urls.static import static
from profile_mgmt import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_auth/', include("user_auth.urls")),
    path('profile_mgmt/', include("profile_mgmt.urls")),
    path('', include("django.contrib.auth.urls")),
    path('reservations/', include("reservations.urls")),
    path('inventory/', include("inventory.urls")),
    path('report/', include("report.urls")),
    path('', include("static_pages.urls")),
    path("", home, name = "home"),
]
