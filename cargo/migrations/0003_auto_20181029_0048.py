# Generated by Django 2.1.2 on 2018-10-29 00:48

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0002_auto_20181027_0057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='role',
        ),
        migrations.AddField(
            model_name='employee',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the employee contact number (e.g. +19999999999, etc.)', max_length=128),
        ),
    ]