from rest_framework import serializers
from .models import BloomFilterModel
from .utils import BloomFilter  # Import the BloomFilter class from utils

class BloomFilterSerializer(serializers.ModelSerializer):
    bit_array = serializers.SerializerMethodField()

    class Meta:
        model = BloomFilterModel
        fields = ['id', 'bit_array', 'size', 'num_hashes','num_characters']

    def get_bit_array(self, obj):
        bf = BloomFilter(size=obj.size, num_hashes=obj.num_hashes)
        bf.bit_array = list(obj.bit_array)
        return bf.bit_array_to_string()

class JacardSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
