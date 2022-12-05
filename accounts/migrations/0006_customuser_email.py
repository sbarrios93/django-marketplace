# Generated by Django 4.1.3 on 2022-12-03 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_remove_customuser_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email",
            field=models.EmailField(default="test", max_length=128, unique=True),
            preserve_default=False,
        ),
    ]
