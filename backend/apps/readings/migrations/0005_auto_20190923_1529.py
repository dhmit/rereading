# Generated by Django 2.2.4 on 2019-09-23 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0004_auto_20190917_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='story',
            name='word_count',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_text',
            field=models.TextField(default=''),
        ),
    ]
