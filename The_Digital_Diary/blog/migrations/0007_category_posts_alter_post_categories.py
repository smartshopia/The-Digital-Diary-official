# Generated by Django 5.0.7 on 2024-08-05 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_category_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='categories_set', to='blog.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='posts_set', to='blog.category'),
        ),
    ]