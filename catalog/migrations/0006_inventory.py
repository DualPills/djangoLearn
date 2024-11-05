# Generated by Django 4.2.16 on 2024-11-05 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_cartitem_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='catalog.book')),
                ('quantity_available', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
            },
        ),
    ]