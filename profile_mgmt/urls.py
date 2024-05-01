#    WORKED ON FILE:
#       - NOEL VARGA (w1932378)
#       - DOMINIC JOBSON (w1892005)

from django.urls import path
from profile_mgmt import views as Vw
from .views import statusUpdate, editStatusPage, updateStatus

urlpatterns = [
    path('user_info/',Vw.user_info, name='user_info'),
    path('update_user/', Vw.update_user, name='update_user'),
    path('statusUpdate/', statusUpdate, name = "statusUpdate"),
    path('editStatusPage/<int:id>', editStatusPage, name = "editStatusPage"),
    path('editStatusPage/updateStatus/<int:id>', updateStatus, name='updateStatus'),
]

