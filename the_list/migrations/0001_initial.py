# Generated by Django 3.0.4 on 2020-03-29 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('purpose', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('disabled', models.BooleanField(default=False)),
                ('leaders', models.ManyToManyField(blank=True, related_name='leader_of', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manage_by', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='member_of', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('for_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_list.ShopGroup')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'for_group')},
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.CharField(blank=True, default='1', max_length=30, null=True)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('date_purchased', models.DateField(blank=True, null=True)),
                ('cancelled', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cancel_by', to=settings.AUTH_USER_MODEL)),
                ('in_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_list.ShopGroup')),
                ('purchased', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buy_by', to=settings.AUTH_USER_MODEL)),
                ('requested', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='req_by', to=settings.AUTH_USER_MODEL)),
                ('to_get_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='the_list.Merchant')),
            ],
            options={
                'ordering': ['description'],
            },
        ),
    ]
