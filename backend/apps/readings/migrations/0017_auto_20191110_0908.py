# Generated by Django 2.2.4 on 2019-11-10 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0016_auto_20191110_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentquestion',
            name='response_word_limit',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='segmentquestion',
            name='response_word_limit',
            field=models.IntegerField(default=0, null=True),
        ),
    ]