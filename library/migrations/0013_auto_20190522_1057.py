# Generated by Django 2.1.7 on 2019-05-22 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_auto_20190518_1352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]