# Generated by Django 5.0.6 on 2024-06-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloomfilter', '0002_remove_bloomfiltermodel_num_hashes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloomfiltermodel',
            name='num_hashes',
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name='bloomfiltermodel',
            name='size',
            field=models.IntegerField(default=1000),
        ),
    ]
