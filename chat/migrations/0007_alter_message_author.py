# Generated by Django 3.2.3 on 2021-06-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]