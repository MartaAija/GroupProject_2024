# Generated by Django 5.0.3 on 2024-04-25 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_equip_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equip_item',
            name='status',
            field=models.CharField(choices=[('decommisioned', 'Dicommisioned'), ('on_loan', 'On loan'), ('available', 'Available'), ('repairing', 'Repairing')], default='available', max_length=20),
        ),
    ]
