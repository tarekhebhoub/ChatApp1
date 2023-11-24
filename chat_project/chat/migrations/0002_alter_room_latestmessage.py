# Generated by Django 3.2.21 on 2023-11-23 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='latestMessage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='the_last_message', to='chat.message'),
        ),
    ]
