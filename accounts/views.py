from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import States, Poll, Political_Parties, constituency_table, Candidates, Aadhar_Details, Voter_Details, User_vote_cast_data, First_Login_Authentication, OTP
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from accounts.face import face
from random import randint
from django.core.mail import send_mail

# Create your views here.

def capture_pic(request,candidate_id):
    name = face(request)
    if name == request.user.username:
        candidate = Candidates.objects.get(id = candidate_id)
        candidate.Votes_Obtained = int(candidate.Votes_Obtained)+1
        candidate.save()
        User_vote_cast_data.objects.create(caster_id=request.user.id,Poll_id=candidate.Poll_id)
        messages.success(request,'Vote was successfully casted')
        return redirect('home')
    else:
        candidate = Candidates.objects.get(id=candidate_id)
        messages.warning(request,'face doesnot match')
        return redirect('cast_vote',candidate.Poll_id)

@login_required(login_url='login')
def authenticate(request):
    if request.user.is_staff:
        return redirect('home')
    else:
        authenticate = True
        if request.method == 'POST':
            mail_id = request.POST.get('mail_id')
            user_details = User.objects.get(id=request.user.id)
            user_details.email = mail_id
            user_details.save()
            range_start = 10**(6-1)
            range_end = (10**6)-1
            otp = randint(range_start,range_end)
            OTP.objects.create(Otp=otp,user_id=request.user.id)
            send_mail(
                'OTP for online Voting',
                'Your otp is: '+str(otp),
                'noreply@gmail.com',
                [mail_id],
            )
            return redirect('otp_validate')
        try:
            first = First_Login_Authentication(user_id=request.user.id)
            range_start = 10**(6-1)
            range_end = (10**6)-1
            otp = randint(range_start,range_end)
            otp_details = OTP.objects.get(user_id=request.user.id)
            otp_details.Otp = otp
            otp_details.save()
            send_mail(
                'OTP for online Voting',
                'Your otp is: '+str(otp),
                'noreply@gmail.com',
                [request.user.email],
            )
            return redirect('otp_validate')
        except:
            return render(request,'pages/authenticate.html',{'authenticate':authenticate})

def otp_validate(request):
    authenticate=True
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        try:
            otp_details = OTP.objects.get(user_id = request.user.id)
            print(otp_details.Otp)
            if otp == otp_details.Otp:
                print("yes")
                First_Login_Authentication.objects.create(Status="Done",user_id=request.user.id)
                return redirect('home')
            else:
                messages.warning(request,'Otp Doesnot Match!')
                return redirect('logout')
        except:
            return redirect('authenticate')
    return render(request,'pages/otp_validate.html',{'authenticate':authenticate})

@login_required(login_url='login')
def end_poll(request,poll_id):
    if not request.user.is_staff:
        return redirect('home')
    poll = Poll.objects.get(id=poll_id)
    if poll.is_Active:
        poll.is_Active = False
        poll.save()
        messages.success(request,'Poll Ended')
        return redirect('typeset','AvailablePolls')

def add_user(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        gardian_type = request.POST.get('gardian_type')
        gardian_name = request.POST.get('gardian_name')
        aadhar_number = request.POST.get('aadhar_number')
        DOB = request.POST.get('DOB')
        gender = request.POST.get('gender')
        door_number = request.POST.get('door_number')
        street = request.POST.get('street')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode= request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')
        voter_id = request.POST.get('voter_id')
        part_no = request.POST.get('part_no')
        part_name = request.POST.get('part_name')
        constituency_no = request.POST.get('constituency_no')
        constituency_name = request.POST.get('constituency_name')
        img = request.FILES['profile_pic']
        fs = FileSystemStorage()
        img.name = aadhar_number+".jpg"
        filename = fs.save(img.name,img)
        user = User.objects.create_user(username=aadhar_number,password=phone_number)
        Aadhar_Details.objects.create(FullName=fullname,Aadhar_Number=aadhar_number,Date_Of_Birth = DOB,Gender = gender,Gardian_Type=gardian_type,Gardian_Name=gardian_name,Phone_Number = phone_number,D_no=door_number,Street = street,City=city,State_Name = state,Pin_Code = pincode,Profile_Picture=filename,user_id = user.id)
        Voter_Details.objects.create(Voter_Id = voter_id,Part_No=part_no,Part_Name=part_name,Constituency_Number=constituency_no,Constituency_Name=constituency_name,user_id=user.id)
        messages.success(request,'Added Successfully')
        return redirect('add_user')
    states = States.objects.all()
    constituencies = constituency_table.objects.filter(Consistituent_State=1)
    return render(request,'pages/add_user.html',{'states':states,'constituencies':constituencies})

@login_required(login_url='login')
def home(request):
    id = request.user.id
    try:
        aadhardetails = Aadhar_Details.objects.get(user_id=id)
    except:
        aadhardetails = None
    states = States.objects.all()
    voterdetails = None
    try:
        voterdetails = Voter_Details.objects.get(user_id = id)
        state = States.objects.get(State_Name=aadhardetails.State_Name)
        polls = Poll.objects.filter(Poll_State_id=state.id)
    except:
        messages.warning(request,'You Cannot participate in any Polls')
        voterdetails = False
        polls = None
    return render(request,'pages/home.html',{'aadhar_details':aadhardetails,'voterdetails':voterdetails,'polls':polls,'states':states})

@login_required(login_url='login')
def profile(request):
    pass

@login_required(login_url='login')
def pollster(request):
    states = States.objects.all()
    if request.method == 'POST':
        poll_description = request.POST.get('poll-desc')
        state = request.POST.get('state')
        print(state)
        print(poll_description)
        state_data = States.objects.get(State_Name = state)
        Poll.objects.create(Poll_Description=poll_description,Poll_State_id=state_data.id)
        messages.success(request,'Poll Added')
        return redirect('typeset','AvailablePolls')
    return render(request,'pages/pollster.html',{'states':states})

@login_required(login_url='login')
def candidate_delete(request,candidate_id):
    candidate = Candidates.objects.get(id=candidate_id)
    if not request.user.is_staff:
        return redirect('home')
    poll = Poll.objects.get(id=candidate.Poll_id)
    candidate.delete()
    messages.success(request,'Candidate Deleted')
    return redirect('edit',poll.id)

@login_required(login_url='login')
def cast_vote(request,poll_id):
    id = request.user.id
    try:
        aadhardetails = Aadhar_Details.objects.get(user_id=id)
    except:
        aadhardetails = None
    poll = Poll.objects.get(id = poll_id)
    if not poll.is_Active:
        candidates = Candidates.objects.filter(Poll_id=poll_id)
        return render(request,'pages/results.html',{'poll':poll,'candidates':candidates})
    states = States.objects.all()
    voterdetails = None
    try:
        voterdetails = Voter_Details.objects.get(user_id = id)
        state = States.objects.get(State_Name=aadhardetails.State_Name)
        try:
            caster_details = User_vote_cast_data.objects.get(Poll_id=poll_id,caster_id=id)
            messages.warning(request,'You have already Casted Your Vote.')
            return redirect('home')
        except:
            pass
        constuency = constituency_table.objects.get(Consistituent_Name = voterdetails.Constituency_Name)
        candidates = Candidates.objects.filter(Constituency_id=constuency.id,Poll_id=poll_id)
        poll = Poll.objects.get(id=poll_id)
    except:
        messages.warning(request,'You Cannot participate in any Polls')
        voterdetails = False
        polls = None
    return render(request,'pages/cast_vote.html',{'aadhar_details':aadhardetails,'states':states,'poll':poll,'state':state,'candidates':candidates})

@login_required(login_url='login')
def authentidate_face(request,candidate_id):
    authenticate = True
    return render(request,'pages/authenticate_face.html',{'authenticate':authenticate,'candidate_id':candidate_id})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def addstate(request):
    if request.method == 'POST' or request.FILES['image-name']:
        state = request.POST.get('state')
        img = request.FILES['image-name']
        fs = FileSystemStorage()
        img.name = state+".jpg"
        filename = fs.save(img.name,img)
        States.objects.create(State_Name = state,State_Image = filename)
        messages.success(request,'State Added')
    return redirect('typeset','AddState')

@login_required(login_url='login')
def addparty(request):
    if request.method == 'POST':
        party_name = request.POST.get('party-name')
        img = request.FILES['image-name']
        fs = FileSystemStorage()
        img.name = party_name+".jpg"
        filename = fs.save(img.name,img)
        Political_Parties.objects.create(Party_Name=party_name,Party_Symbol=filename)
        messages.success(request,'Party Name Added')
    return redirect('typeset','AddPartyName')

@login_required(login_url='login')
def typeset(request,name):
    states = States.objects.all()
    state_info = None
    poll_info = None
    parties = None
    if name == 'AddState':
        type = 'AddState'
    elif name == 'AddConstitution':
        type = 'AddConstitution'
        states = States.objects.all()
    elif name == 'AddPartyName':
        type = 'AddPartyName'
        parties = Political_Parties.objects.all()
    elif name == 'AvailablePolls':
        poll_info = Poll.objects.filter(is_Active=True)
        type = 'AvailablePolls'
    return render(request,'pages/home.html',{'type':type,'states':states,'polls':poll_info,'parties':parties})

@login_required(login_url='login')
def addconstitution(request):
    if request.method == 'POST':
        constitution_name = request.POST.get('constitution_name')
        state_name = request.POST.get('state_name')
        state_info = States.objects.get(State_Name=state_name)
        constituency_table.objects.create(Consistituent_Name=constitution_name,Consistituent_State_id=state_info.id)
        messages.success(request,'Consistuency Added')
    return redirect('typeset','AddConstitution')

@login_required(login_url='login')
def edit(request,poll_id):
    if not request.user.is_staff:
        return redirect('home')
    poll = Poll.objects.get(id = poll_id)
    if request.method == 'POST':
        poll_description = request.POST.get('poll_description')
        if poll_description != poll.Poll_Description:
            poll.Poll_Description = poll_description
            poll.save()
            messages.success(request,'Poll Description Updated')
            return redirect('edit',poll_id)
    state_info = States.objects.all()
    candidates = Candidates.objects.filter(Poll_id = poll_id)
    return render(request,'pages/edit.html',{'poll':poll,'states':state_info,'candidates':candidates})

@login_required(login_url='login')
def add_choice(request,poll_id):
    if not request.user.is_staff:
        return redirect('home')
    poll = Poll.objects.get(id=poll_id)
    if request.method == 'POST':
        is_individual = request.POST.get('is_individual')
        if is_individual == 'yes':
            candidate_name = request.POST.get('candidate_name')
            constituency_name = request.POST.get('constituency_name')
            independent_candidate_party = request.POST.get('independent_candidate_party')
            img = request.FILES['independent_party_image']
            fs = FileSystemStorage()
            img.name = independent_candidate_party+".jpg"
            filename = fs.save(img.name,img)
            constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
            Candidates.objects.create(Candidate_Name=candidate_name,Constituency_id=constituency.id,Party=independent_candidate_party,Party_PIC=filename,Candidate_Type='independent',Poll_id=poll.id)
            messages.success(request,'Candidate Added')
            return redirect('edit',poll_id)
        elif is_individual == None:
            candidate_name = request.POST.get('candidate_name')
            constituency_name = request.POST.get('constituency_name')
            candidate_party = request.POST.get('candidate_party')
            party = Political_Parties.objects.get(Party_Name=candidate_party)
            constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
            Candidates.objects.create(Candidate_Name=candidate_name,Constituency_id=constituency.id,Party=candidate_party,Party_PIC=party.Party_Symbol,Candidate_Type='not independent',Poll_id=poll.id)
            messages.success(request,'Candidate Added')
            return redirect('edit',poll_id)
    parties = Political_Parties.objects.all()
    constituencies = constituency_table.objects.filter(Consistituent_State_id = poll.Poll_State_id)
    return render(request,'pages/add_choice.html',{'parties':parties,'constituencies':constituencies,'poll':poll})

@login_required(login_url='login')
def candidate_edit(request,candidate_id):
    if not request.user.is_staff:
        return redirect('home')
    parties = Political_Parties.objects.all()
    candidate = Candidates.objects.get(id = candidate_id)
    poll = Poll.objects.get(id = candidate.Poll_id)
    if request.method == 'POST':
        if candidate.Candidate_Type == 'independent':
            try:
                img = request.FILES['independent_party_image']
                candidate_name = request.POST.get('candidate_name')
                constituency_name = request.POST.get('constituency_name')
                independent_candidate_party = request.POST.get('independent_candidate_party')
                constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
                candidate.Candidate_Name = candidate_name
                candidate.Constituency_id = constituency.id
                candidate.Party = independent_candidate_party
                fs = FileSystemStorage()
                img.name = independent_candidate_party+".jpg"
                filename = fs.save(img.name,img)
                candidate.Party_PIC = filename
                candidate.save()
                messages.success(request,'Candidate Details Updates')
                return redirect('edit',poll.id)
            except:
                candidate_name = request.POST.get('candidate_name')
                constituency_name = request.POST.get('constituency_name')
                independent_candidate_party = request.POST.get('independent_candidate_party')
                constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
                candidate.Candidate_Name = candidate_name
                candidate.Constituency_id = constituency.id
                candidate.Party = independent_candidate_party
                candidate.save()
                messages.success(request,'Candidate Details Updated')
                return redirect('edit',poll.id)
        else:
            candidate_name = request.POST.get('candidate_name')
            constituency_name = request.POST.get('constituency_name')
            candidate_party = request.POST.get('candidate_party')
            party = Political_Parties.objects.get(Party_Name=candidate_party)
            #constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
            constituency = constituency_table.objects.get(Consistituent_Name=constituency_name)
            candidate.Candidate_Name = candidate_name
            candidate.Constituency_id = constituency.id
            candidate.Party = candidate_party
            candidate.Party_PIC = party.Party_Symbol
            candidate.save()
            messages.success(request,'Candidate Details Updated')
            return redirect('edit',poll.id)
    constituencies = constituency_table.objects.filter(Consistituent_State_id=poll.Poll_State_id)
    return render(request,'pages/add_choice.html',{'candidate':candidate,'poll':poll,'edit_candidate':True,'constituencies':constituencies,'parties':parties})

@login_required(login_url='login')
def delete_poll(request,poll_id):
    poll = Poll.objects.get(id = poll_id)
    if not request.user.is_staff:
        return redirect('home')
    poll.delete()
    messages.success(request,'Poll Deleted Successfully')
    return redirect('typeset','AvailablePolls')

@login_required(login_url='login')
def endpoll(request,poll_id):
    pass

def login(request):
    if isauthenticate(request):
        return redirect('authenticate')
    else:
        if request.method == 'POST':
            anumber = request.POST.get('anumber')
            pnumber = request.POST.get('pnumber')
            user = auth.authenticate(username=anumber,password=pnumber)

            if user is not None:
                auth.login(request,user)
                return redirect('authenticate')
            else:
                messages.warning(request,'Invalid username or password')
                return redirect('login')
        return render(request,'pages/login.html')

def isauthenticate(request):
    if request.user.is_authenticated:
        return True
    else:
        return False