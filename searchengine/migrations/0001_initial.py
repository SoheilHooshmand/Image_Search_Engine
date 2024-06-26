# Generated by Django 5.0.6 on 2024-06-25 09:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=50)),
                ('brand_id', models.PositiveIntegerField(blank=True, null=True)),
                ('brand_name', models.CharField(blank=True, max_length=100, null=True)),
                ('category_id', models.PositiveIntegerField(blank=True, null=True)),
                ('category_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender_id', models.PositiveIntegerField(blank=True, null=True)),
                ('gender_name', models.CharField(blank=True, max_length=100, null=True)),
                ('shop_id', models.PositiveIntegerField(blank=True, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=50)),
                ('current_price', models.PositiveIntegerField(default=0)),
                ('old_price', models.PositiveIntegerField(default=0)),
                ('off_percent', models.PositiveIntegerField(default=0)),
                ('update_date', models.DateTimeField(null=True)),
                ('colors', models.ManyToManyField(to='searchengine.color')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='searchengine.image')),
                ('sizes', models.ManyToManyField(to='searchengine.size')),
            ],
        ),
    ]
