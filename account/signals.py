from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from mvt.models import CareSeeker
from mvt.models import CareTaker
from account.models import User

@receiver(post_save,sender = User)
def set_user_group(sender,instance,created,*args,**kwargs):

    if created:
        user = Group.objects.get(name = 'user')
        instance.groups.add(user)

        if instance.role == 'CT':
            ct = Group.objects.get(name='care_taker')
            instance.groups.add(ct)
            CareTaker.objects.create(care_taker = instance)
        
        if instance.role == 'CS':
            cs = Group.objects.get(name='care_seeker')
            instance.groups.add(cs)
            CareSeeker.objects.create(care_seeker = instance)
