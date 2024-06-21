from django.db import models

class BloomFilterModel(models.Model):
    bit_array = models.BinaryField(null=True)
    size = models.IntegerField(default=1000)
    num_hashes = models.IntegerField(default=15)
    num_characters = models.IntegerField(default=0)