# Generated by Django 5.0.6 on 2024-06-20 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloomfilter', '0003_bloomfiltermodel_num_hashes_bloomfiltermodel_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloomfiltermodel',
            name='num_characters',
            field=models.IntegerField(default=0),
        ),
    ]
