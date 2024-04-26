"""
URL configuration for school_IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from static_pages.views import home
from inventory import views as inventoryViews
from static_pages.views import home
from static_pages.views import termsnconditions
from static_pages.views import contactus
from static_pages.views import about
from static_pages.views import history
from static_pages.views import faq
from static_pages.views import privacy
from django.conf.urls.static import static
from django.conf import settings
from profile_mgmt import views as Vw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_auth/', include("user_auth.urls")),
    path('profile_mgmt/', include("profile_mgmt.urls")),
    path('', include("django.contrib.auth.urls")),
    path('reservations/', include("reservations.urls")),
    path('inventory/', include("inventory.urls")),
    path("termsnconditions/", termsnconditions, name = "termsnconditions"),
    path("contactus/", contactus, name = "contactus"),
    path("about/", about, name = "about"),
    path("faq/", faq, name = "faq"),
    path("history/", history, name = "history"),
    path("privacy/", privacy, name = "privacy"),
    path('report/', include("report.urls")),
    path("", home, name = "home"),
]
