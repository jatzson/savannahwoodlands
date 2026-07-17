import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('property_type', models.CharField(choices=[('land', 'Land'), ('agricultural_land', 'Agricultural Land'), ('duplex', 'Duplex'), ('detached_house', 'Detached House'), ('bungalow', 'Bungalow'), ('terrace', 'Terrace House'), ('apartment', 'Apartment / Flat'), ('commercial', 'Commercial Property')], max_length=30)),
                ('status', models.CharField(choices=[('for_sale', 'For Sale'), ('new_development', 'New Development'), ('under_offer', 'Under Offer'), ('sold', 'Sold')], default='for_sale', max_length=20)),
                ('location', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('bedrooms', models.PositiveIntegerField(blank=True, null=True)),
                ('bathrooms', models.PositiveIntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, help_text='e.g. 650 sqm, 2 plots', max_length=100)),
                ('price', models.CharField(blank=True, help_text='e.g. ₦45,000,000', max_length=100)),
                ('price_on_request', models.BooleanField(default=False)),
                ('main_image', models.ImageField(upload_to='properties/main/')),
                ('is_featured', models.BooleanField(default=False, help_text='Show this property on the homepage')),
                ('is_active', models.BooleanField(default=True, help_text='Uncheck to hide without deleting')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Properties',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='properties/gallery/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='events.property')),
            ],
        ),
    ]
