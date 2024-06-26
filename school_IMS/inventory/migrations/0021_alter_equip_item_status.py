# Generated by Django 5.0.3 on 2024-04-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_alter_equip_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip_item',
            name='status',
            field=models.CharField(choices=[('decommisioned', 'Dicommisioned'), ('available', 'Available'), ('repairing', 'Repairing'), ('on_loan', 'On loan')], default='available', max_length=20),
        ),
    ]
