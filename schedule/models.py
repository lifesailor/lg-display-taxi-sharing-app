from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

# Create your models here
class Schedule(models.Model):
    objects = models.Manager()
    
    time = models.CharField(max_length=50)
    day = models.IntegerField(blank=True) #요일(sunday=0, modnay=1, tuesday=2, wednesday=3, thursday=4, friday=5, saturday=6, holiday=7)
    fromLocation = models.CharField(max_length=50, default="월롱역")
    toLocation = models.CharField(max_length=50, default="기숙사")
    transport = models.IntegerField(default = 0) #지하철: 0, 순환 버스: 1, 복귀 버스: 2
    
    reserved_users = models.ManyToManyField(User, blank=True, through='Reserve', related_name="reserved_users")

    def __str__(self):
        return self.time
    
    @property
    def reserve_count(self):
        return self.reserve_set.filter(created_date = date.today()).count()

class Reserve(models.Model):
    user = models.ForeignKey(User)
    schedule = models.ForeignKey(Schedule)
    created_date = models.DateField(default=timezone.now)
 