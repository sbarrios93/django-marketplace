# Generated by Django 4.1.3 on 2022-12-03 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_rename_identifier_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email",
            field=models.EmailField(default="a@a.com", max_length=128, unique=True),
            preserve_default=False,
        ),
    ]
