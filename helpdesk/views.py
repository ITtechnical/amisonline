from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,get_user_model,update_session_auth_hash
from django.core.paginator import Paginator
import datetime
from django.contrib.auth.models import User
from .import models
from .models import Profile,Ticket,Ticket_Comments,Escalate,AssignedTicket,Technician,EscalatedTicket,Status,Region,District
from .forms import UserTicket,UserLoginForm,Agent_Ticket,agent_detail_Ticket,Ticket_comment,Escalade,Edit_Agent_Ticket,CreateUserForm,ProfileUserForm,Edit_helpdesk_Ticket,ViewTicket,EditProfileUserForm
# from django.db.models import Sum ,Q,Count
from .filters import TicketFilter
from django.contrib.auth.decorators import login_required
from amis.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_PHONE_NUMBER
from django.core.mail import send_mail,EmailMessage
from django.db.models import Sum ,Q,Count
from twilio.rest import TwilioRestClient
from twilio.rest import Client
# from .decorators import unauthenticated_user


@login_required
def closed_ticket(request):
    cc = request.user.profile.id
    profile = Profile.objects.get(id=cc)
    if profile.is_staff == True:
        total = Ticket.objects.filter(name=profile,status= 1).order_by('-id')
    elif profile.is_agent == True:
        total = AssignedTicket.objects.filter(name=profile,status= 1).order_by('-ticketid')
    else:
        total = Ticket.objects.filter(status= 1).order_by('-id')
    template= "helpdesk/closedticket.html"
    context ={
             'total':total,
    }
    return render(request,template,context)

@login_required
def open_ticket(request):
    cc = request.user.profile.id
    profile = Profile.objects.get(id=cc)
    if profile.is_staff == True:
        total = Ticket.objects.filter(name=profile,status= 2).order_by('-id')
    elif profile.is_agent == True:
        total = AssignedTicket.objects.filter(name=profile,status= 2).order_by('-ticketid')
    else:
        total = Ticket.objects.filter(status= 2).order_by('-id')
    template= "helpdesk/opened.html"
    context ={
             'total':total,
    }
    return render(request,template,context)

@login_required
def solved_ticket(request):
    cc = request.user.profile.id
    profile = Profile.objects.get(id=cc)
    if profile.is_staff == True:
        total = Ticket.objects.filter(name=profile,astatus= 1).order_by('-id')
    elif profile.is_agent == True:
        total = AssignedTicket.objects.filter(name=profile,astatus= 1).order_by('-ticketid')
    elif profile.is_admin == True:
        total = Ticket.objects.filter(astatus= 1).order_by('-id')
    else:
        total = Ticket.objects.filter(escalated= 'Escalate').order_by('-id')
    template= "helpdesk/solved.html"
    context ={
             'total':total,
    }
    return render(request,template,context)

@login_required
def total_ticket(request):
    cc = request.user.profile.id
    profile = Profile.objects.get(id=cc)
    if profile.is_staff == True:
        total = Ticket.objects.filter(name=profile).order_by('-id')
    elif profile.is_agent == True:
        total = AssignedTicket.objects.filter(name=profile).order_by('-ticketid')
    else:
        total = Ticket.objects.all().order_by('-id')
    template= "helpdesk/solved.html"
    context ={
             'total':total,
    }
    return render(request,template,context)

# @login_required
def dashboard(request):
    today = datetime.datetime.now()
    total = Ticket.objects.all().order_by('-id')
    total_ticket = total.filter(ticket_date__year=today.year).count()
    escalated_ticket = total.filter(escalated='Escalate',ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    regional_ticket = Ticket.objects.values('region').order_by('region').annotate(S = Count('region'))


    template="helpdesk/dashboard.html"
    context ={
            'total':total,'total_ticket':total_ticket,
            'ticket_solved':ticket_solved,'ticket_pending':ticket_pending,
            'ticket_closed':ticket_closed, 'escalated_ticket':escalated_ticket,
            'regional_ticket':regional_ticket
    }
    return render(request,template,context)

@login_required
def helpdesk_dashboard(request):
    today = datetime.datetime.now()
    total = Ticket.objects.all().order_by('-id')
    total_ticket = total.filter(ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    page = request.GET.get('page', 1)
    paginator = Paginator(total, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    template = 'helpdesk/helpdesk_dashboard.html'
    context ={'users':users,'total':total,'total_ticket':total_ticket,
                     'ticket_solved':ticket_solved,'ticket_pending':ticket_pending,
                     'ticket_closed':ticket_closed}
    return render(request, template, context)

@login_required
def agent_escalated(request):
    today = datetime.datetime.now()
    profile = request.user.profile.id

    total = EscalatedTicket.objects.filter(name=profile).order_by('-ticketid')

    total_ticket = total.filter(ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    paginator = Paginator(total, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    template = 'helpdesk/agent_escalated.html'
    context ={'users':users,'total':total,'total_ticket':total_ticket,
                     'ticket_solved':ticket_solved,'ticket_pending':ticket_pending,
                     'ticket_closed':ticket_closed}
    return render(request, template, context)

@login_required
def agent_dashboard(request):
    today = datetime.datetime.now()
    total = request.user.profile.assignedticket_set.all().order_by('-ticketid')
    total_ticket = total.filter(ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    paginator = Paginator(total, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    template = 'helpdesk/agent_dashboards.html'
    context ={'users':users,'total':total,'total_ticket':total_ticket,
                     'ticket_solved':ticket_solved,'ticket_pending':ticket_pending,
                     'ticket_closed':ticket_closed}
    return render(request, template, context)

@login_required()
def user_dashboard(request):
    today = datetime.datetime.now()
    total = request.user.profile.ticket_set.all().order_by('-id')
    totals = total.filter(status=2).order_by('-id')
    total_ticket = total.filter(ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    paginator = Paginator(totals, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    page = request.GET.get('page', 1)

    template = 'helpdesk/user_dashboard.html'
    context ={'total':total,'totals':totals,'total_ticket':total_ticket,
                     'ticket_solved':ticket_solved,'ticket_pending':ticket_pending,
                     'ticket_closed':ticket_closed}
    return render(request, template, context)

@login_required
def user_ticket(request):
    #if this is a POST request we need to process the form data
    if request.method == 'POST':
        #create a form instance and populate it with the data from the request:
        form = UserTicket(request.POST)
        #check whether the process data in the form is valid:
        if form.is_valid():
            #Now process the data in form.clearned_data as required
            ticket= form.save(commit=False)
            #get the profile id of the user
            userprofile = request.user.profile.id
            #search for the profile using the  profile id
            searchprofile = Profile.objects.get(id=userprofile)
            #Now link user raising ticket to the ticket
            ticket.name = searchprofile

            ticket.status= Status.objects.get(status_name="open")
            ticket.region = searchprofile.region
            ticket.district = searchprofile.district
            ticket.remarks = "Created by User"
            #commit the linked record to the database
            ticket.save()

            # user_email = searchprofile.email
            user_phone = searchprofile.telephone
            user_name = searchprofile.name
            to = "user_phone"
            client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
            tid= ticket.id
            tsub = ticket.subject
            tstatus = ticket.status
            try:
                message = client.messages.create(
                    to= "+233" + user_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear"+ " "+ user_name+ "," +" " + "Your ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"will be prioritized, assigned and tracked to completion. You will be informed when completed. --Thank you")
                messages.info(request,'Ticket created successfully')
                return redirect('helpdesk:userdashboard')
            except IOError:
                messages.info(request,'Ticket created successfully')
                return redirect('helpdesk:userdashboard')

    else:
        form =UserTicket()
    template = 'helpdesk/user_new_ticket.html'
    context ={'form':form}
    return render (request,template,context)

@login_required
def view_user_ticket(request, pk):
    ticket= Ticket.objects.get(id= pk)
    form = ViewTicket(instance = ticket)
    template = 'helpdesk/user_ticket_detail.html'
    context ={'ticket':ticket,'form':form}
    return render (request,template,context)

@login_required
def edit_user_ticket(request, pk):
    ticket= Ticket.objects.get(id= pk)

    #if this is a POST request we need to process the form data
    if request.method == 'POST':
        #create a form instance and populate it with the data from the request:
        form = UserTicket(request.POST, instance = ticket)
        #check whether the process data in the form is valid:
        if form.is_valid():
            #Now process the data in form.clearned_data as required
            ticket= form.save(commit=False)
            #get the profile id of the user
            userprofile = request.user.profile.id
            #search for the profile using the  profile id
            searchprofile = Profile.objects.get(id=userprofile)

            ticket.save()

            messages.success(request,'Ticket created successfully')
            return redirect('helpdesk:userdashboard')
    else:
        form =UserTicket(instance=ticket)
    template = 'helpdesk/user_new_ticket.html'
    context ={'form':form}
    return render (request,template,context)

@login_required
def agent_ticket(request):
    #if this is a POST request we need to process the form data
    if request.method == 'POST':
        staffid = request.POST.get("staffid")
        staff = User.objects.get(username=staffid)
        mail= staff.email

        #create a form instance and populate it with the data from the request:
        form = Agent_Ticket(request.POST)
        #check whether the process data in the form is valid:
        if form.is_valid():
            #Now process the data in form.clearned_data as required
            ticket= form.save(commit=False)
            #get the profile id of the user
            print(ticket.id)
            userprofile = staff.profile
            #search for the profile using the  profile id

            #Now link user raising ticket to the ticket
            ticket.name = userprofile
            ticket.region = userprofile.region
            ticket.district = userprofile.district
            ticket.remarks = "Created by Helpdesk agent"
            get_agent = ticket.agent.id

            ticket.save()
            user_phone = userprofile.telephone
            user_name = userprofile.name
            client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
            tid= ticket.id
            tsub = ticket.subject
            tstatus= ticket.status
            try:
                message = client.messages.create(
                    to= "+233" + user_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear"+ " "+ user_name+ "," +" " + "Your ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"will be prioritized, assigned and tracked to completion. You will be informed when completed. --Thank you")
            except IOError:
                pass
            search_technician = Technician.objects.get(id=get_agent)
            dd = search_technician.technician
            agentprofile= Profile.objects.get(id=dd.id)
            cc= AssignedTicket.objects.create(ticketid=ticket.id,name =agentprofile, subject=ticket.subject,description = ticket.description, prority=ticket.prority,ticket_date=ticket.ticket_date,expected_date=ticket.expected_date,status=ticket.status,astatus=ticket.astatus)

            tid= cc.ticketid
            tsub = cc.subject
            tstatus= cc.status
            user_phone= agentprofile.telephone
            user_name =agentprofile.name
            try:
                message = client.messages.create(
                    to= "+233" + user_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body="Dear"+ " "+ user_name+ "," +" " +"Ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"has been assigned to you.")
            except IOError:
                pass
            messages.success(request,'Ticket created successfully')
            return redirect('helpdesk:helpdeskdashboard')
    else:
        form =Agent_Ticket()
    template = 'helpdesk/agent_ticket.html'
    context ={'form':form}
    return render (request,template,context)

@login_required
def edit_heldesk_ticket(request, pk):
    try:
        cc= AssignedTicket.objects.get(ticketid= pk)
    except AssignedTicket.DoesNotExist:
        cc = None
    try:
        vv = EscalatedTicket.objects.get(ticketid=pk)
    except EscalatedTicket.DoesNotExist:

        vv = None

    # ticketno = cc.ticketid
    find_ticket = Ticket.objects.get(id = pk)
    if request.method == 'POST':
        form = Edit_helpdesk_Ticket(request.POST, instance = find_ticket)

        if form.is_valid():
            ticket= form.save()
            try:
                cc= AssignedTicket.objects.get(ticketid= pk)
                cc.subject = ticket.subject
                cc.description = ticket.description
                cc.prority = ticket.prority
                cc.ticket_date = ticket.ticket_date
                cc.expected_date = ticket.expected_date
                cc.status = ticket.status
                cc.astatus = ticket.astatus
                cc.save()
            except AssignedTicket.DoesNotExist:
                get_agent = ticket.agent.id

                search_technician = Technician.objects.get(id=get_agent)
                dd = search_technician.technician

                agentprofile= Profile.objects.get(id=dd.id)

                cc = AssignedTicket.objects.create(ticketid=ticket.id,name =agentprofile, subject=ticket.subject,description = ticket.description, prority=ticket.prority,ticket_date=ticket.ticket_date,expected_date=ticket.expected_date,status=ticket.status,astatus=ticket.astatus)

                client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
                tid= cc.ticketid
                tsub = cc.subject
                tstatus= cc.status
                user_phone= agentprofile.telephone
                user_name =agentprofile.name
                try:
                    message = client.messages.create(
                        to= "+233" + user_phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear"+ " "+ user_name+ "," +" " +"Ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"has been assigned to you.")
                except IOError:
                    pass
            try:
                vv= EscalatedTicket.objects.get(ticketid= pk)
                vv.subject = ticket.subject
                vv.description = ticket.description
                vv.ticket_date = ticket.ticket_date
                vv.expected_date = ticket.expected_date
                vv.status = ticket.status
                vv.astatus = ticket.astatus
                vv.save()
            except EscalatedTicket.DoesNotExist:
                get_agent = ticket.agent.id

                search_technician = Technician.objects.get(id=get_agent)
                dd = search_technician.technician

                agentprofile= Profile.objects.get(id=dd.id)

                vv = EscalatedTicket.objects.create(ticketid=ticket.id,name =agentprofile, subject=ticket.subject,description = ticket.description, ticket_date=ticket.ticket_date,expected_date=ticket.expected_date,status=ticket.status,astatus=ticket.astatus)

            if request.user.profile.is_agent == True:
                return redirect("helpdesk:agentdashboard")
            else:
                return redirect("helpdesk:helpdeskdashboard")
    else:
        form =Edit_helpdesk_Ticket(instance= find_ticket)

    template = 'helpdesk/helpdesk_ticket_edit.html'
    context ={'form':form,'find_ticket':find_ticket}
    return render (request,template,context)

@login_required
def edit_agent_ticket(request, pk):
    try:
        cc= AssignedTicket.objects.get(ticketid= pk)
    except AssignedTicket.DoesNotExist:
        cc = None
    try:
        vv = EscalatedTicket.objects.get(ticketid=pk)
    except EscalatedTicket.DoesNotExist:

        vv = None

    # ticketno = cc.ticketid
    find_ticket = Ticket.objects.get(id = pk)
    if request.method == 'POST':
        form = Edit_Agent_Ticket(request.POST, instance = find_ticket)

        if form.is_valid():
            ticket= form.save()
            try:
                cc= AssignedTicket.objects.get(ticketid= pk)
                cc.subject = ticket.subject
                cc.description = ticket.description
                cc.prority = ticket.prority
                cc.ticket_date = ticket.ticket_date
                cc.expected_date = ticket.expected_date
                cc.status = ticket.status
                cc.astatus = ticket.astatus
                cc.save()
            except AssignedTicket.DoesNotExist:
                get_agent = ticket.agent.id

                search_technician = Technician.objects.get(id=get_agent)
                dd = search_technician.technician

                agentprofile= Profile.objects.get(id=dd.id)

                cc = AssignedTicket.objects.create(ticketid=ticket.id,name =agentprofile, subject=ticket.subject,description = ticket.description, prority=ticket.prority,ticket_date=ticket.ticket_date,expected_date=ticket.expected_date,status=ticket.status,astatus=ticket.astatus)
            try:
                vv= EscalatedTicket.objects.get(ticketid= pk)
                vv.subject = ticket.subject
                vv.description = ticket.description
                vv.ticket_date = ticket.ticket_date
                vv.expected_date = ticket.expected_date
                vv.status = ticket.status
                vv.astatus = ticket.astatus
                vv.save()
            except EscalatedTicket.DoesNotExist:
                get_agent = ticket.agent.id

                search_technician = Technician.objects.get(id=get_agent)
                dd = search_technician.technician

                agentprofile= Profile.objects.get(id=dd.id)

                vv = EscalatedTicket.objects.create(ticketid=ticket.id,name =agentprofile, subject=ticket.subject,description = ticket.description, ticket_date=ticket.ticket_date,expected_date=ticket.expected_date,status=ticket.status,astatus=ticket.astatus)

            if request.user.profile.is_agent == True:
                return redirect("helpdesk:agentdashboard")
            else:
                return redirect("helpdesk:helpdeskdashboard")
    else:
        form =Edit_Agent_Ticket(instance= find_ticket)

    template = 'helpdesk/agent_ticket_edit.html'
    context ={'form':form,'find_ticket':find_ticket}
    return render (request,template,context)



@login_required
def escalate_ticket(request,pk):
    today = datetime.datetime.now()
    try:
        vv = EscalatedTicket.objects.get(ticketid=pk)
    except EscalatedTicket.DoesNotExist:
        vv = None
    find_ticket= Ticket.objects.get(id=pk)

    if request.method == 'POST':

        form =Escalade(request.POST)

        if form.is_valid():

            escal= form.save(commit=False)
            escal.ticket_id= find_ticket
            escal.escalated_date = today
            escal.save()

            find_ticket.escalated = "Escalate"
            find_ticket.save()

            get_agent = escal.agent.id
            search_technician = Technician.objects.get(id=get_agent)
            dd = search_technician.technician

            agentprofile= Profile.objects.get(id=dd.id)
            try:
                vv = EscalatedTicket.objects.get(ticketid=pk)
                vv.delete()
                cc= EscalatedTicket.objects.create(ticketid=find_ticket.id,name =agentprofile, subject=find_ticket.subject,description = find_ticket.description,ticket_date=find_ticket.ticket_date,expected_date=find_ticket.expected_date,status=find_ticket.status,astatus=find_ticket.astatus)

                client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
                tid= cc.ticketid
                tsub = cc.subject
                user_phone= agentprofile.telephone
                user_name = agentprofile.name
                try:
                    message = client.messages.create(
                        to= "+233" + user_phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear"+ " "+ user_name+ "," +" " +"Ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"has been escalated to you.")
                except IOError:
                    pass

            except EscalatedTicket.DoesNotExist:
                cc=EscalatedTicket.objects.create(ticketid=find_ticket.id,name =agentprofile, subject=find_ticket.subject,description = find_ticket.description,ticket_date=find_ticket.ticket_date,expected_date=find_ticket.expected_date,status=find_ticket.status,astatus=find_ticket.astatus)

                client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
                tid= cc.ticketid
                tsub = cc.subject
                user_phone= agentprofile.telephone
                user_name = agentprofile.name
                try:
                    message = client.messages.create(
                        to= "+233" + user_phone,
                        from_=TWILIO_PHONE_NUMBER,
                        body="Dear"+ " "+ user_name+ "," +" " +"Ticket with the id"+" "+ tid + " "+"and subject"+" "+" "+"'" + tsub+"'"+" "+" "+"has been escalated to you.")
                except IOError:
                    pass
            messages.success(request,'Ticket Escalated successfully')
            return redirect('helpdesk:agentdashboard')

    else:
        form =Escalade(request.POST)
    template = 'helpdesk/escalate.html'
    context ={'form':form,'find_ticket':find_ticket}
    return render (request,template,context)

@login_required
def detail_agent_ticket(request, pk):
    today = datetime.datetime.now()
    find_ticket = Ticket.objects.get(id = pk)
    ticket_detal = Ticket_Comments.objects.filter(ticket_id = pk)
    escalated_details = Escalate.objects.filter(ticket_id = pk)

    ticketcoment=Ticket_comment()

    if request.method == 'POST':
        #create a form instance and populate it with the data from the request:
        ticketcoment=Ticket_comment(request.POST)
        #check whether the process data in the form is valid:
        if ticketcoment.is_valid():
            #Now process the data in form.clearned_data as required
            comment= ticketcoment.save(commit=False)
            comment.ticket_id = find_ticket
            agentprofile = request.user.id
            #search for the profile using the  profile id
            searchprofile = User.objects.get(id=agentprofile)
            tech = Technician.objects.get(technician=searchprofile.profile)


            comment.agent = tech
            comment.creation_date = today
            comment.save()

            messages.success(request,'Comment created successfully')
            #return redirect('helpdesk:userdashboard')


    template = 'helpdesk/try.html'
    context ={'ticketcoment':ticketcoment,
              'find_ticket':find_ticket,
               'ticket_detal':ticket_detal,
               'escalated_details':escalated_details}
    return render (request,template,context)


 # render login page with the request and context
# @unauthenticated_user
def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST ) #create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
        if form.is_valid(): # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
            username = form.cleaned_data.get('username') # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
            password = form.cleaned_data.get('password') # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
            user = authenticate(username=username, password=password) # re-authenticate the username and password and store it into variable called user
            if user is not  None:
                login(request,user)
                type_obj = Profile.objects.get(user = user)
                if request.user.profile.is_new == True:
                    return redirect('helpdesk:profile')
                elif type_obj.is_agent: #if user passes the authentication and his object_type is == is_director
                    return redirect ('helpdesk:agentdashboard') # redirect the user to the director homepage
                elif  type_obj.is_staff:  #if user passes the authentication and his object_type is == is_standard
                    return redirect('helpdesk:userdashboard') # redirect the user to the standard user homepage
                elif type_obj.is_admin:  #if user passes the authentication and his object_type is == is_standard
                     return redirect('helpdesk:helpdeskdashboard')
                elif type_obj.is_director:  #if user passes the authentication and his object_type is == is_standard
                     return redirect('helpdesk:dirsearch')
            else:
                messages.info(request,'Username or Password is incorrect')
                return redirect ("helpdesk:login") # redirect the user to the managers



    context = {
                'form': form, #context is the form itself
        }
    return render(request,'helpdesk/index.html',context)

def logout_request(request):
    logout(request) #passout the request as an argument to the logout() function
    return redirect("helpdesk:login") # redirect to the login page

# @unauthenticated_user
def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user.refresh_from_db()
            type_obj = Profile.objects.get(user = user)
            if user.is_authenticated and request.user.profile.is_new == True:
                return redirect('helpdesk:profile')
            elif user.is_authenticated and type_obj.is_agent: #if user passes the authentication and his object_type is == is_director
                return redirect ('helpdesk:agentdashboard') # redirect the user to the director homepage
            elif user.is_authenticated and type_obj.is_staff:  #if user passes the authentication and his object_type is == is_standard
                return redirect('helpdesk:userdashboard') # redirect the user to the standard user homepage
            elif user.is_authenticated and type_obj.is_admin:  #if user passes the authentication and his object_type is == is_standard
                 return redirect('helpdesk:helpdeskdashboard')
            elif user.is_authenticated and type_obj.is_director:  #if user passes the authentication and his object_type is == is_standard
                 return redirect('helpdesk:dirsearch')

    template='helpdesk/signup.html'
    context= {'form':form

    }
    return render(request,template, context)

@login_required
def profile(request):
    find_profile = Profile.objects.get(id=request.user.profile.id)
    form = ProfileUserForm(instance=find_profile)
    if request.method == 'POST':
        form =ProfileUserForm(request.POST,instance=find_profile)
        if form.is_valid():
            user = form.save()
            user.is_new = False
            user.save()
            user.refresh_from_db()
            type_obj = user

            if type_obj.is_agent:
                return redirect ('helpdesk:agentdashboard')
            elif type_obj.is_staff:
                return redirect('helpdesk:userdashboard')
            elif type_obj.is_admin:
                 return redirect('helpdesk:helpdeskdashboard')

    template='helpdesk/profile.html'
    context= {'form':form,
               'find_profile':find_profile

    }
    return render(request,template, context)


@login_required
def editprofile(request):
    find_profile = Profile.objects.get(id=request.user.profile.id)
    form = EditProfileUserForm(instance=find_profile)
    if request.method == 'POST':
        form =EditProfileUserForm(request.POST,instance=find_profile)
        if form.is_valid():
            user = form.save()
            user.is_new = False
            user.save()
            user.refresh_from_db()
            type_obj = user

            if type_obj.is_agent:
                return redirect ('helpdesk:agentdashboard')
            elif type_obj.is_staff:
                return redirect('helpdesk:userdashboard')
            elif type_obj.is_admin:
                 return redirect('helpdesk:helpdeskdashboard')

    template='helpdesk/profile.html'
    context= {'form':form,
               'find_profile':find_profile

    }
    return render(request,template, context)

@login_required
def agent_search(request):

    total = request.user.profile.assignedticket_set.all()

    myFilter = TicketFilter(request.GET, queryset=total)
    total = myFilter.qs
    total.order_by('-ticketid')
    total_all = total.count()

    template = 'helpdesk/agentsearch.html'
    context ={'myFilter':myFilter,'total':total,'total_all':total_all}
    return render(request, template, context)

@login_required
def search(request):

    total = Ticket.objects.all()

    myFilter = TicketFilter(request.GET, queryset=total)
    total = myFilter.qs
    total_all = total.count()

    template = 'helpdesk/search.html'
    context ={'myFilter':myFilter,'total':total,'total_all':total_all}
    return render(request, template, context)

def load_district(request):
    region_id = request.GET.get('region')
    district = District.objects.filter(region=region_id).order_by('districtname')
    return render(request, 'helpdesk/district_dropdown_list.html', {'district': district})

def load_agent(request):
    agent_id = request.GET.get('team')
    agent = Technician.objects.filter(team=agent_id).order_by('technician')
    return render(request, 'helpdesk/agent_dropdown_list.html', {'agent': agent})

def closeticket(request, pk):
    find_ticket = Ticket.objects.get(id=pk)
    find_ticket.status == 1
    find_ticket.save()
    return redirect('helpdesk:edittickethelp',pk)

@login_required
def dirsearch(request):
    today = datetime.datetime.now()

    total = Ticket.objects.all()
    total_ticket = total.filter(ticket_date__year=today.year).count()
    escalated_ticket = total.filter(escalated='Escalate',ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    myFilter = TicketFilter(request.GET, queryset=total)
    total = myFilter.qs
    total_ticket = total.filter(ticket_date__year=today.year).count()
    escalated_ticket = total.filter(escalated='Escalate',ticket_date__year=today.year).count()
    ticket_solved = total.filter(astatus= 1,ticket_date__year=today.year).count()
    ticket_pending = total.filter(status=2,ticket_date__year=today.year).count()
    ticket_closed = total.filter(status=1,ticket_date__year=today.year).count()

    template = 'helpdesk/dirsearch.html'
    context ={'myFilter':myFilter,'total':total,'total_ticket':total_ticket,
              'escalated_ticket':escalated_ticket,'ticket_solved':ticket_solved,
              'ticket_pending':ticket_pending,'ticket_closed':ticket_closed}
    return render(request, template, context)
