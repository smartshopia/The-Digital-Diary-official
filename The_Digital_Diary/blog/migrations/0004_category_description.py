# Generated by Django 5.0.7 on 2024-08-05 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_post_likes_post_share_count_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]