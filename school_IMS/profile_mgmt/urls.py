from django.urls import path
from profile_mgmt import views as Vw
from .views import statusUpdate, editStatusPage, updateStatus

urlpatterns = [
path('user_info/',Vw.user_info, name='user_info'),
path('statusUpdate/', statusUpdate, name = "statusUpdate"),
path('editStatusPage/<int:id>', editStatusPage, name = "editStatusPage"),
path('editStatusPage/updateStatus/<int:id>', updateStatus, name='updateStatus'),
]

