# Generated by Django 5.1.2 on 2024-12-18 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_kiado', '0018_alter_book_options_alter_cart_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio_en',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
        migrations.AddField(
            model_name='profile',
            name='bio_hu',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
    ]
