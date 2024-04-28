# Generated by Django 4.0 on 2024-04-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='available_items',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]