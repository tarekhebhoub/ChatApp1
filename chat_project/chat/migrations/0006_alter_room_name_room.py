# Generated by Django 3.2.21 on 2023-11-26 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_message_readby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name_room',
            field=models.CharField(max_length=255),
        ),
    ]
