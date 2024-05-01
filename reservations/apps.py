from django.apps import AppConfig

# Define a custom configuration class for the 'reservations' app
class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'
