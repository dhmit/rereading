# Generated by Django 2.2.4 on 2019-11-10 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0012_auto_20191101_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentsegmentdata',
            name='scroll_ups',
        ),
        migrations.RemoveField(
            model_name='studentsegmentdata',
            name='views',
        ),
        migrations.AddField(
            model_name='studentsegmentdata',
            name='is_rereading',
            field=models.BooleanField(default=None),
        ),
        migrations.AddField(
            model_name='studentsegmentdata',
            name='scroll_data',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='studentsegmentdata',
            name='view_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='documentquestion',
            name='response_word_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='documentquestionresponse',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_question', to='readings.DocumentQuestion'),
        ),
        migrations.AlterField(
            model_name='segmentquestion',
            name='response_word_limit',
            field=models.IntegerField(default=0),
        ),
    ]
