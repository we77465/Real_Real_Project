from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class UploadeModel(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)  # 使用DateTimeField，并添加auto_now_add=True
    descript = models.CharField(max_length=50)
    original_img = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.user_id
    
class DownloadModel(models.Model):
    user_id = models.CharField(max_length=50)
    download_time = models.CharField(max_length=50)
    download_wm_len = models.CharField(max_length=50)