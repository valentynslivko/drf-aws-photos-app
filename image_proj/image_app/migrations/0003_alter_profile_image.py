# Generated by Django 5.0.7 on 2024-08-04 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("image_app", "0002_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.CharField(blank=True, null=True),
        ),
    ]
