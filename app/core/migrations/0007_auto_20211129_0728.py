# Generated by Django 2.2 on 2021-11-29 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20211129_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingrdients',
            new_name='ingredients',
        ),
    ]
