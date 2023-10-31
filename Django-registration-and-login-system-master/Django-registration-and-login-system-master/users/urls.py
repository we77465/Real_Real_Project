from django.urls import path
from .views import home, profile, RegisterView,download_image,delete_image

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('download-image/<int:image_id>/', download_image, name='download_image'),
    path('delete-image/<int:image_id>/', delete_image, name='delete_image'),
]
