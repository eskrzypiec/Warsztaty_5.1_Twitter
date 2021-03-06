# Generated by Django 2.1.4 on 2018-12-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tweet',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
