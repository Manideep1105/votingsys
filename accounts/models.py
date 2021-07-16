from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone

# Create your models here.

class States(models.Model):
    State_Name = models.CharField(max_length=50)
    State_Image = models.ImageField()

    def __str__(self):
        return [self.State_Name,self.State_Image]

class Poll(models.Model):
    Poll_Description = models.TextField()
    is_Active = models.BooleanField(default=True)
    Publish_Date = models.DateTimeField(default=timezone.now)
    Make_Visible = models.BooleanField(default=False)
    Poll_State = models.ForeignKey(States,on_delete=models.CASCADE)

class Political_Parties(models.Model):
    Party_Name = models.CharField(max_length=100)
    Party_Symbol = models.ImageField()

class constituency_table(models.Model):
    Consistituent_Name = models.CharField(max_length=50)
    Consistituent_State = models.ForeignKey(States,on_delete=models.CASCADE)

class Candidates(models.Model):
    Candidate_Name = models.CharField(max_length=255)
    Constituency = models.ForeignKey(constituency_table,on_delete=models.CASCADE)
    Party = models.CharField(max_length=255)
    Party_PIC = models.ImageField()
    Candidate_Type = models.CharField(max_length=20)
    Votes_Obtained = models.CharField(max_length=10,default=0)
    Poll = models.ForeignKey(Poll,on_delete=models.CASCADE)

class Aadhar_Details(models.Model):
    FullName = models.CharField(max_length=225)
    Aadhar_Number = models.CharField(max_length=15)
    Date_Of_Birth = models.CharField(max_length=30)
    Gender = models.CharField(max_length=10)
    Gardian_Type = models.CharField(max_length=10)
    Gardian_Name = models.CharField(max_length=225)
    Phone_Number = models.CharField(max_length=13)
    D_no = models.CharField(max_length=15)
    Street = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State_Name = models.CharField(max_length=100)
    Pin_Code = models.CharField(max_length=15)
    Profile_Picture = models.ImageField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Voter_Details(models.Model):
    Voter_Id = models.CharField(max_length=50)
    Part_No = models.CharField(max_length=5)
    Part_Name = models.CharField(max_length=50)
    Constituency_Number = models.CharField(max_length=10)
    Constituency_Name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class User_vote_cast_data(models.Model):
    caster = models.ForeignKey(User,on_delete=models.CASCADE)
    Poll = models.ForeignKey(Poll,on_delete=models.CASCADE)

class First_Login_Authentication(models.Model):
    Status = CharField(max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class OTP(models.Model):
    Otp = models.CharField(max_length=10)
    user = models.ForeignKey(User,on_delete=models.CASCADE)