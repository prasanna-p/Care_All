from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    role_types = [("CS","care_seeker"),("CT","care_taker")]
    genders = [('M',"Male"),('F',"Female")]
    
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=500,blank=True,default="I love to write blogs......")
    image = models.ImageField(default='default.jpg',upload_to="proflie/",blank=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=5,blank=True,choices=genders)
    address = models.TextField(blank=True)
    contact = models.IntegerField(null=True)
    role = models.CharField(max_length=20,blank=True,choices=role_types)

    def save(self,*args,**kwargs):

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def get_absolute_url(self):
        return reverse("profile",kwargs = {'pk':self.pk})
    
    def __str__(self):

        return self.username
    
    def check_review(self,cs,ct):
            request = cs.requests.filter(care_taker=ct).filter(status="CM").latest("timestamp")
            if request:
                review = self.Reviews_given.filter(request_ob=request)
                if review:
                    return False
                else:
                    return True
            return False
    
    def check_review1(self,request):
        review = self.Reviews_given.filter(request_ob=request)
        if review:
            return False
        else:
            return True





# Create your models here.
