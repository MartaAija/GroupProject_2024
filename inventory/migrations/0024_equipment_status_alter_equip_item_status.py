# Generated by Django 5.0.3 on 2024-04-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_alter_equip_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('On-Loan', 'On-Loan'), ('In-Repair', 'In-Repair'), ('Decommisioned', 'Decommisioned')], default='Available', max_length=20),
        ),
        migrations.AlterField(
            model_name='equip_item',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('on_loan', 'On loan'), ('decommisioned', 'Dicommisioned'), ('repairing', 'Repairing')], default='available', max_length=20),
        ),
    ]