from os import name
from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('pollster/',views.pollster,name='pollster'),
    path('logout/',views.logout,name='logout'),
    path('home/<str:name>/',views.typeset,name='typeset'),
    path('addstate/',views.addstate,name='addstate'),
    path('addparty/',views.addparty,name='addparty'),
    path('addconstitution/',views.addconstitution,name='addconstitution'),
    path('end/<int:poll_id>/', views.endpoll, name='end_poll'),
    path('edit/<int:poll_id>/',views.edit,name='edit'),
    path('add_choice/<int:poll_id>/',views.add_choice,name='add_choice'),
    path('candidate_edit/<int:candidate_id>/',views.candidate_edit,name='candidate_edit'),
    path('delete_poll/<int:poll_id>/',views.delete_poll,name='delete_poll'),
    path('candidate_delete/<int:candidate_id>/',views.candidate_delete,name='candidate_delete'),
    path('add_user/',views.add_user,name='add_user'),
    path('cast_vote/<int:poll_id>/',views.cast_vote,name='cast_vote'),
    path('authentidate_face/<int:candidate_id>/',views.authentidate_face,name='authentidate_face'),
    path('capture_pic/<int:candidate_id>',views.capture_pic,name='capture_pic'),
    path('authenticate/',views.authenticate,name='authenticate'),
    path('otp_validate/',views.otp_validate,name='otp_validate'),
    path('end_poll/<int:poll_id>/',views.end_poll,name = 'end_poll'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)