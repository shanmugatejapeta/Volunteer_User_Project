from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Problems(models.Model):
    statement=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    solution=models.TextField(default="Not Yet Resolved!")
    resolved=models.BooleanField(default=False)

    def __str__(self):
        return self.statement
    
    
class Volunteers(models.Model):
    vol=models.TextField()
    vol_id=models.IntegerField()
    def __str__(self):
        return self.vol
    
class VUser(models.Model):
    vol=models.ForeignKey(Volunteers,on_delete=models.CASCADE,related_name='users')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='vols')
    def __str__(self):
        return self.vol.vol+' - '+self.user.username
    

