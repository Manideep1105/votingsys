# Generated by Django 3.2.3 on 2021-06-25 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_candidates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voter_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Voter_Id', models.CharField(max_length=50)),
                ('Part_No', models.CharField(max_length=5)),
                ('Part_Name', models.CharField(max_length=50)),
                ('Constituency_Number', models.CharField(max_length=10)),
                ('Constituency_Name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Aadhar_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FullName', models.CharField(max_length=225)),
                ('Aadhar_Number', models.CharField(max_length=15)),
                ('Date_Of_Birth', models.CharField(max_length=30)),
                ('Gender', models.CharField(max_length=10)),
                ('Gardian_Type', models.CharField(max_length=10)),
                ('Gardian_Name', models.CharField(max_length=225)),
                ('Phone_Number', models.CharField(max_length=13)),
                ('D_no', models.CharField(max_length=15)),
                ('Street', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=100)),
                ('State_Name', models.CharField(max_length=100)),
                ('Pin_Code', models.CharField(max_length=15)),
                ('Profile_Picture', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
