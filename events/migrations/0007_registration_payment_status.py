from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_property_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending Payment'), ('confirmed', 'Payment Confirmed')], default='pending', max_length=20),
        ),
    ]
