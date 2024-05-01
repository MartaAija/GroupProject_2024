from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from .models import ReservationDetails, Equipment
from django.contrib.auth import get_user_model

class ReservationDetailsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test data that will be used by all test methods in this class
        cls.equipment = Equipment.objects.create(display_name='Test Equipment', quantity=10)
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_create_valid_reservation(self):
        # Test creating a valid reservation instance
        valid_reservation = ReservationDetails.objects.create(
            equipment=self.equipment,
            quantity=2,
            reserved_date=timezone.now(),
            return_date=timezone.now() + timedelta(days=14),
            user=self.user,
            status=ReservationDetails.PENDING
        )
        self.assertEqual(str(valid_reservation), f"Reservation for {self.equipment.display_name}")
        self.assertEqual(valid_reservation.quantity, 2)
        self.assertEqual(valid_reservation.status, ReservationDetails.PENDING)

    def test_invalid_reservation_creation(self):
        # Test creating an invalid reservation instance (e.g., negative quantity)
        with self.assertRaises(ValidationError):
            invalid_reservation = ReservationDetails(
                equipment=self.equipment,
                quantity=-1,  # Invalid quantity
                reserved_date=timezone.now(),
                return_date=timezone.now() + timedelta(days=14),
                user=self.user,
                status=ReservationDetails.PENDING
            )
            invalid_reservation.full_clean()  # Trigger validation and raise ValidationError

    def test_clean_method_validation(self):
        # Test clean method to validate reservation details
        # Test invalid quantity (negative)
        with self.assertRaises(ValidationError):
            invalid_quantity_reservation = ReservationDetails(
                equipment=self.equipment,
                quantity=-1,
                reserved_date=timezone.now(),
                return_date=timezone.now() + timedelta(days=14),
                user=self.user,
                status=ReservationDetails.PENDING
            )
            invalid_quantity_reservation.full_clean()

        # Test reserved date in the past
        with self.assertRaises(ValidationError):
            past_date_reservation = ReservationDetails(
                equipment=self.equipment,
                quantity=1,
                reserved_date=timezone.now() - timedelta(days=1),  # Reserved date in the past
                return_date=timezone.now() + timedelta(days=14),
                user=self.user,
                status=ReservationDetails.PENDING
            )
            past_date_reservation.full_clean()

    def test_signal_receiver(self):
        # Test signal receiver function for updating equipment quantity
        initial_quantity = self.equipment.quantity
        
        # Create a reservation
        reservation = ReservationDetails.objects.create(
            equipment=self.equipment,
            quantity=3,
            reserved_date=timezone.now(),
            user=self.user,
            status=ReservationDetails.PENDING
        )
        
        # Verify quantity reduction after reservation creation
        self.assertEqual(self.equipment.quantity, initial_quantity - 3)

        # Update reservation status to completed and verify quantity restoration
        reservation.status = ReservationDetails.COMPLETED
        reservation.save()
        self.assertEqual(self.equipment.quantity, initial_quantity)
