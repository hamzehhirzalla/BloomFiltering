from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
    path('redirect_to_user/', RedirectView.as_view(url=reverse_lazy('current-user')), name='redirect-to-user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
