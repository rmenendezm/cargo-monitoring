# Generated by Django 2.1.2 on 2018-10-17 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0002_auto_20181011_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='dispatcher',
            field=models.ForeignKey(blank=True, help_text='Represents the employee from a carrier company who close the deal with the broker', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dispatcher', to='cargo.Employee'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='driver',
            field=models.ForeignKey(blank=True, help_text='Represents the employee from a carrier company who was assigned for delivering the cargo', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='driver', to='cargo.Employee'),
        ),
    ]