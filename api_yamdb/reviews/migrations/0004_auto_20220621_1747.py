# Generated by Django 2.2.16 on 2022-06-21 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220621_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review'),
        ),
    ]
