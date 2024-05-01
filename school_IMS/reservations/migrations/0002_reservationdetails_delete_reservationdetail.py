# Generated by Django 5.0.3 on 2024-04-25 15:27

import django.db.models.deletion
import django.utils.timezone
import reservations.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_equip_item_status'),
        ('reservations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('reserved_date', models.DateField(default=django.utils.timezone.now)),
                ('return_date', models.DateField(default=reservations.models.default_return_date)),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.equipment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_view_reservation', 'Can view reservation'), ('can_modify_reservation', 'Can modify reservation'), ('can_delete_reservation', 'Can delete reservation')],
            },
        ),
        migrations.DeleteModel(
            name='ReservationDetail',
        ),
    ]