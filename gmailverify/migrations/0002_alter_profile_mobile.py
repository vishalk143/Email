# Generated by Django 4.2.1 on 2023-06-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmailverify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mobile',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]