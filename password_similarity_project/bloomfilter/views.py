from rest_framework import status, views
from rest_framework.response import Response
from .models import BloomFilterModel
from .serializers import *
from .utils import BloomFilter
from rest_framework import serializers

'''
Function to train the application bloom filter on a list of password that will be giving by the user in the post request
Post request requires list of passwords, size of the array, and the number of hash functions to be used
The function will return the bloom filter array, with a unique ID for the new bloom filter
'''
class TrainBloomFilterView(views.APIView):
    def post(self, request):
        passwords = request.data.get('passwords', [])
        size = request.data.get('size', 1000)
        num_hashes = request.data.get('num_hashes', 15)
        num_characters=request.data.get('num_characters',0)
        bf = BloomFilter(size=size, num_hashes=num_hashes)
        for password in passwords:
            password= ' '+password+' '
            bf.add(password)
        
        bf_model = BloomFilterModel(size=size, num_hashes=num_hashes,num_characters=num_characters)
        bf.save_to_model(bf_model)
        
        serializer = BloomFilterSerializer(bf_model)
        response_data = serializer.data
        response_data['bit_array'] = bf.bit_array_to_string()
        return Response(response_data, status=status.HTTP_201_CREATED)

'''
Function to test if a password is in the bloom filter or not using a post reuqest
The function will just test the password, but will not save it to the bloom filter
The ID of the bloom filter to test on must be included in the URL path
'''
class TestPasswordView(views.APIView):
    def post(self, request, pk):
        try:
            bf_model = BloomFilterModel.objects.get(pk=pk)
        except BloomFilterModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bf = BloomFilter.load_from_model(bf_model)
        
        password = request.data.get('password')
        password = ' '+password+' '
        threshold = request.data.get('threshold', 0.827)
        
        result = bf.check(password, threshold)
        return Response({'result': result}, status=status.HTTP_200_OK)

'''
Return all the bloom filters that exists in the application, with their information
'''
class GetAllBloomFiltersView(views.APIView):
    def get(self, request):
        bloom_filters = BloomFilterModel.objects.all()
        serializer = BloomFilterSerializer(bloom_filters, many=True)
        
        response_data = serializer.data
        for bloom_filter in response_data:
            bf = BloomFilter(size=bloom_filter['size'], num_hashes=bloom_filter['num_hashes'])
            bf.bit_array = list(BloomFilterModel.objects.get(id=bloom_filter['id']).bit_array)
            bloom_filter['bit_array'] = bf.bit_array_to_string()
        
        return Response(response_data, status=status.HTTP_200_OK)
'''
Delete a specific bloom filter using its ID
'''
class DeleteBloomFilterView(views.APIView):
    def delete(self, request, pk):
        try:
            bloom_filter = BloomFilterModel.objects.get(pk=pk)
            bloom_filter.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BloomFilterModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

'''
Post Funcion to return the similarity percentage of two passwords, using accard coefficient
Two passwords should be included in the post function
'''
class JaccardCoefficientView(views.APIView):
    serializer_class = JacardSerializer  
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():  
            password1 = serializer.validated_data['password1']
            password1 =' '+password1+' '
            password2 = serializer.validated_data['password2']
            password2 =' '+password2+' '
            bf1 = BloomFilter(size=1000, num_hashes=15)
            bf1.add(password1)

            bf2 = BloomFilter(size=1000, num_hashes=15)
            bf2.add(password2)

            jaccard_similarity = self.jaccard_coefficient(bf1, bf2)
            return Response({'jaccard_similarity': jaccard_similarity}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def jaccard_coefficient(self, bloom_filter1, bloom_filter2):
        gamma_beta1_beta2 = sum(1 for i in range(bloom_filter1.size) if bloom_filter1.bit_array[i] and bloom_filter2.bit_array[i])
        k_beta1 = sum(bloom_filter1.bit_array)
        k_beta2 = sum(bloom_filter2.bit_array)

        return gamma_beta1_beta2 / (k_beta1 + k_beta2 - gamma_beta1_beta2) if (k_beta1 + k_beta2 - gamma_beta1_beta2) > 0 else 0
