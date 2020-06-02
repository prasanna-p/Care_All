from django.db import models
from account.models import User
from django.urls import reverse
from django.utils.dateparse import parse_date
from datetime import date,timedelta

# Create your models here.
class CareTaker(models.Model):

    care_taker = models.OneToOneField(User,on_delete = models.CASCADE)
    savings = models.IntegerField(blank=True,default=0)
    active_caretaker_count = models.IntegerField(default=0)

    def __str__(self):
        return self.care_taker.username

    def get_absolute_url(self):
        return reverse("caretaker",kwargs={'pk':self.pk})
    
    
    def care_seeker_duplication(self):
        request_list = self.requested.all()
        completed_list = self.requested.filter(status='CM')
        return [ request.care_seeker for request in request_list if request not in completed_list ]

    
    def get_care_seeker(self,obj):
        try:

            res = self.requested.filter(care_seeker=obj).latest('timestamp')
            return res


        except Request.DoesNotExist:

            return None
    
    def get_care_seekers(self):
        return self.requested.all()
    
    def get_care_taker_name(self):
        return self.care_taker.username

    
    def get_care_taker_email(self):
        return self.care_taker.email 

    
    def get_care_taker_contact(self):
        return self.care_taker.contact

    
    def get_care_taker_pk(self):
        return self.pk

    
    def get_care_taker_image(self):
        return self.care_taker.image.url

    
    def get_age(self):
        return self.care_taker.age

    
    def get_bio(self):
        return self.care_taker.bio

    def get_address(self):
        return self.care_taker.address 
    
    def check_request(self,obj):
        request = self.requested.filter(care_seeker=obj).filter(status="PE")
        if not request:
            return True
        else:
            return False
    
    def end_service(self,bill):
        self.savings+=bill
        self.active_caretaker_count-=1
        self.save()
    
    def get_request_object(self,obj):
        request = self.requested.filter(care_seeker=obj).filter(status="CM").latest('timestamp')
        return request



    


class CareSeeker(models.Model):

    care_seeker = models.OneToOneField(User,on_delete=models.CASCADE)
    care_taker = models.ForeignKey(CareTaker,on_delete=models.CASCADE,related_name="care_seekers",blank=True,null=True)
    wallet =models.IntegerField(blank=True,default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):

        return self.care_seeker.username

    def get_absolute_url(self):
        return reverse("care_seeker",kwargs={'pk':self.pk})
    
    def get_care_seeker_name(self):
        return self.care_seeker.username

    
    def get_care_seeker_email(self):
        return self.care_seeker.email 

    
    def get_care_seeker_contact(self):
        return self.care_seeker.contact

    
    def get_care_seeker_pk(self):
        return self.pk

    
    def get_care_seeker_image(self):
        return self.care_seeker.image.url

    
    def get_age(self):
        return self.care_seeker.age

    
    def get_bio(self):
        return self.care_seeker.bio

    def get_address(self):
        return self.care_seeker.address
    
    def get_request(self):

        try:
            return self.requests.filter(status='PE')
        
        except Request.DoesNotExist:
            return None 
    
    def get_care_taker_status(self,obj):

        request = self.requests.filter(care_taker=obj).latest('timestamp')
        if request.status == 'PE':
            return False
        else:
            return request.get_status()
    
    def get_request_object(self,obj):
        request = self.requests.filter(care_taker=obj).filter(status="CM").latest('timestamp')
        return request

    
    def check_balance(self):
        return self.wallet
    
    def add_fund(self,fund):

        self.wallet+=int(fund)
        self.save()
    
    def approve_request(self,ct,obj):
        request = self.requests.filter(care_taker=ct).filter(status="PE").latest("timestamp")
        request.start_date = obj["start_date"]
        request.end_date = obj["end_date"]
        request.status = 'AP'
        request.save()
        self.is_available = False
        self.care_taker = ct
        ct.active_caretaker_count+=1
        ct.save()
        self.save()
    
    def calculatefund(self,obj):
        perday_amount = 300
        start_day = parse_date(obj['start_date'])
        end_day = parse_date(obj['end_date'])
        total_days = end_day-start_day
        bill = total_days.days * perday_amount
        return bill
    
    def end_service(self,bill):
        self.is_available = True
        self.wallet-=bill
        self.care_taker = None
        self.save()

  

class FundTransferRecord(models.Model):

    payer = models.ForeignKey(CareSeeker,on_delete=models.CASCADE,related_name="transaction_history",null=True)
    reciver = models.ForeignKey(CareTaker,on_delete=models.CASCADE,related_name="transaction_history",null=True)
    ammount = models.IntegerField(blank=True,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payer.care_seeker.username



class Request(models.Model):

    request_status = [("AP","approved"),('PE','pending'),('RE',"rejected"),('CM',"completed"),('AC',"active")]

    care_seeker = models.ForeignKey(CareSeeker,on_delete=models.CASCADE,related_name="requests",blank=True,null=True)
    care_taker = models.ForeignKey(CareTaker,on_delete=models.CASCADE,related_name="requested",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=10,choices=request_status,null=True)



    def __str__(self):
        return self.care_seeker.care_seeker.username


    def get_status(self):
        res = [request[1] for request in Request.request_status if self.status == request[0]]
        return res[0]


    def get_care_seeker_name(self):
        return self.care_seeker.care_seeker.username

    
    def get_care_seeker_email(self):
        return self.care_seeker.care_seeker.email 

    
    def get_care_seeker_contact(self):
        return self.care_seeker.care_seeker.contact

    
    def get_care_seeker_pk(self):
        return self.care_seeker.pk

    
    def get_care_seeker_image(self):
        return self.care_seeker.care_seeker.image.url
    
    def get_care_taker_name(self):
        return self.care_taker.care_taker.username

    
    def get_care_taker_email(self):
        return self.care_taker.care_taker.email 

    
    def get_care_taker_contact(self):
        return self.care_taker.care_taker.contact

    
    def get_care_taker_pk(self):
        return self.care_taker.pk

    
    def get_care_taker_image(self):
        return self.care_taker.care_taker.image.url
    
    def get_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d")
    
    def get_startdate(self):
        return self.start_date
    
    def get_enddate(self):
        return self.end_date
    

    def get_pk(self):
        return self.pk

    def start_service(self):
        self.status = 'AC'
        self.save()

    def end_service(self):
        self.status = "CM"
        self.save()
        perday_amount = 300
        total_days = self.end_date-self.start_date
        bill = total_days.days*perday_amount
        return bill
    
    def reject_request(self):

        self.status = "RE"
        self.save()
    
    def auto_rejection(self):
        day = date.today()+timedelta(days=5)
        self.end_date = day
        self.save()
    
    
class Review(models.Model):

    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Reviews_given",null=True)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Reviews_taken",null=True)
    request_ob = models.ForeignKey(Request,on_delete=models.CASCADE,related_name="reviews",null=True)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    msg = models.TextField()
    rating = models.FloatField()

    # def __str__(self):
    #     return self.from_user.username

    

    





















# class post(models.Model):
#     statuses = [
#         ("D","draft"),
#         ("p","published")
#         ]
#     title = models.CharField(max_length=50)
#     slug = models.SlugField(blank=True,unique=True)
#     content = models.TextField()
#     date = models.DateField(auto_now=True)
#     status = models.CharField(max_length=1,choices=statuses)
#     image = models.ImageField(upload_to="blog/post",blank=True)
#     Catogary= models.ForeignKey(Catogary,on_delete=models.CASCADE,related_name="posts")
#     author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts",null=True)
    

#     def __str__(self):
#         return self.title

#     def save(self,*args,**kwargs):

#         self.slug = slugify(self.title)
#         super().save(*args,**kwargs)
    
#     def get_absolute_url(self):
#         return reverse("post_detail",kwargs = {"slug":self.slug})
