# Generated by Django 2.2 on 2019-05-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_blogpost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]