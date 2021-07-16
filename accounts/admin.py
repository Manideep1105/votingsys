from django.contrib import admin
from accounts.models import States,Poll,Political_Parties,constituency_table, Candidates, Aadhar_Details, Voter_Details, User_vote_cast_data, First_Login_Authentication, OTP

# Register your models here.

admin.site.register(States)
admin.site.register(Poll)
admin.site.register(Political_Parties)
admin.site.register(constituency_table)
admin.site.register(Candidates)
admin.site.register(Aadhar_Details)
admin.site.register(Voter_Details)
admin.site.register(User_vote_cast_data)
admin.site.register(First_Login_Authentication)
admin.site.register(OTP)