import django.db.models.deletion
import events.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_property_propertyimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PropertyImage',
        ),
        migrations.CreateModel(
            name='PropertyMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Upload a photo or a video clip', upload_to=events.models.property_media_path)),
                ('media_type', models.CharField(blank=True, choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='events.property')),
            ],
            options={
                'ordering': ['order', 'uploaded_at'],
            },
        ),
    ]
