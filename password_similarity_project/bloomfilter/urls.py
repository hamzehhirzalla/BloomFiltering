from django.urls import path
from .views import *

urlpatterns = [
    path('train/', TrainBloomFilterView.as_view(), name='train_bloomfilter'),
    path('test/<int:pk>/', TestPasswordView.as_view(), name='test_password'),
    path('all/', GetAllBloomFiltersView.as_view(), name='get_all_bloom_filters'),
    path('delete/<int:pk>/', DeleteBloomFilterView.as_view(), name='delete_bloom_filter'),
    path('jaccard/', JaccardCoefficientView.as_view(), name='jaccard_coefficient'),
]
