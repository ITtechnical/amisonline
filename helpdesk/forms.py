from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from .import models
from datetime import date
from .models import Technician, Profile,District,Region,Team, Technician

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class UserTicket(forms.ModelForm):
    # ticket_date = forms.DateField(label=False)
    """docstring for UserTicket."""

    class Meta():
        model= models.Ticket
        fields=('subject','ticket_date', 'description')

        widgets = {
                 'ticket_date': DateInput(),
                 'subject': forms.TextInput(attrs={'placeholder':'Subject...'}),
                 'description': forms.Textarea(attrs={'placeholder':'Type a message...'}),
        }

        labels = {
               'ticket_date':'Ticket Date',
               'subject': 'Subject',
               'description':'Description',

        }

class ViewTicket(forms.ModelForm):
    # ticket_date = forms.DateField(label=False)
    """docstring for UserTicket."""

    class Meta():
        model= models.Ticket
        fields=('subject','ticket_date', 'description','status','agent')

        widgets = {
                 'ticket_date': DateInput(attrs={'readonly':'readonly'}),
                 'subject': forms.TextInput(attrs={'readonly':'readonly'}),
                 'description': forms.Textarea(attrs={'readonly':'readonly'}),
                 'status': forms.TextInput(attrs={'readonly':'readonly'}),
                 'agent': forms.TextInput(attrs={'readonly':'readonly'}),
        }

        labels = {
               'ticket_date':'Ticket Date',
               'subject': 'Subject',
               'description':'Description',
               'status':'Ticket Status',
               'agent':'Assigned Agent',

        }


class Agent_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model= models.Ticket
        fields=('subject','ticket_date', 'agent_team','agent','prority','expected_date','description','status')

        widgets = {
                 'ticket_date': DateInput(),
                 'subject': forms.TextInput(attrs={'placeholder':'Subject...'}),
                 'description': forms.Textarea(attrs={'placeholder':'Type a message...'}),
                 'expected_date': DateInput(),
        }

        labels = {
               'subject': 'Subject',
               'ticket_date': 'Date',
               'agent_team':'Team',
               'agent':'Agent',
               'prority':'Prority',
               'expected_date': 'Estimated Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Technician.objects.none()

        if 'agent_team' in self.data:
            try:
                agent_id = int(self.data.get('agent_team'))
                self.fields['agent'].queryset = Technician.objects.filter(team=agent_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['district'].queryset = self.instance.region.district_set.order_by('district_name')


class Edit_helpdesk_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model= models.Ticket
        fields=('subject','ticket_date', 'agent_team','agent','prority','expected_date','description','astatus','status')

        widgets = {
                 'ticket_date': DateInput(attrs={'readonly':'readonly'}),
                 'subject': forms.TextInput(attrs={'readonly':'readonly'}),
                 'description': forms.Textarea(attrs={'readonly':'readonly'}),
                 'astatus': forms.TextInput(attrs={'readonly':'readonly'}),
                 # 'agent': forms.TextInput(attrs={'readonly':'readonly'}),
                 # 'prority': forms.TextInput(attrs={'readonly':'readonly'}),
                 'expected_date': DateInput(attrs={'readonly':'readonly'}),
        }

        labels = {
               'subject': 'Subject',
               'ticket_date': 'Date',
               'agent_team':'Team',
               'agent':'Agent',
               'prority':'Prority',
               'status': 'Ticket Status',
               'astatus': 'Agent Status',
               'expected_date': 'Estimated Date',
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['agent'].queryset = Technician.objects.none()
    #
    #     if 'agent_team' in self.data:
    #         try:
    #             agent_id = int(self.data.get('agent_team'))
    #             self.fields['agent'].queryset = Technician.objects.filter(team=agent_id)
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['agent'].queryset = self.instance.agent_team.technician_set.order_by('technician')


class Edit_Agent_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():
        model= models.Ticket
        fields=('subject','ticket_date', 'agent_team','agent','prority','expected_date','description','astatus','status')

        widgets = {
                 'ticket_date': DateInput(attrs={'readonly':'readonly'}),
                 'subject': forms.TextInput(attrs={'readonly':'readonly'}),
                 'description': forms.Textarea(attrs={'readonly':'readonly'}),
                 'agent_team': forms.TextInput(attrs={'readonly':'readonly'}),
                 'agent': forms.TextInput(attrs={'readonly':'readonly'}),
                 'status': forms.TextInput(attrs={'readonly':'readonly'}),
                 'prority': forms.TextInput(attrs={'readonly':'readonly'}),
                 'expected_date': DateInput(attrs={'readonly':'readonly'}),
        }

        labels = {
               'subject': 'Subject',
               'ticket_date': 'Date',
               'agent_team':'Team',
               'agent':'Agent',
               'prority':'Prority',
               'status': 'Ticket Status',
               'astatus': 'Agent Status',
               'expected_date': 'Estimated Date',
        }


class agent_detail_Ticket(forms.ModelForm):
    """docstring for AgentTicket."""

    class Meta():

        model= models.Ticket
        fields=( 'status','prority','escalated')


        labels = {

               'escalated': 'Status',
               'agent_team':'Team',
               'agent':'Agent',
               'prority':'Prority',

        }

class Ticket_comment(forms.ModelForm):
    content =forms.CharField(label=False, widget = forms.Textarea(attrs={'placeholder':'Type a message...'}))
    """docstring for AgentTicket."""

    class Meta():
        model= models.Ticket_Comments
        fields=( 'content',)

class Escalade(forms.ModelForm):
    reason =forms.CharField(label=False, widget = forms.Textarea(attrs={'placeholder':'Type a message...'}))
    """docstring for AgentTicket."""

    class Meta():
        model= models.Escalate
        fields=( 'agent','agent_team','reason')

        labels = {
               'agent':'Agent',
               'agent_team':'Team',
               'reason': 'Reason'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Technician.objects.none()

        if 'agent_team' in self.data:
            try:
                agent_id = int(self.data.get('agent_team'))
                self.fields['agent'].queryset = Technician.objects.filter(team=agent_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['district'].queryset = self.instance.region.district_set.order_by('district_name')


class UserLoginForm(forms.Form):
    username =forms.CharField(label=False, widget = forms.TextInput(attrs={'placeholder':'Password'}))
    password = forms.CharField(label=False,widget = forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self,*args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username or Password incorrect')
            if not user.check_password(password):
                raise forms.ValidationError('Username or Password incorrect')
            if not user.is_active:
                raise forms.ValidationError('Username or Password incorrect')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta():
        model= models.User
        fields = ('username','password')


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label=False, widget = forms.TextInput(attrs={'placeholder':'Username'}))
    first_name = forms.CharField(label=False, widget = forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(label=False, widget = forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(label=False, widget = forms.TextInput(attrs={'placeholder':'Email'}))
    password1 = forms.CharField(label=False,widget = forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label=False,widget = forms.PasswordInput(attrs={'placeholder':'Comfirm Password'}))

    class Meta:
        model =User
        fields=['username','first_name','last_name','email','password1','password2']

    def clean(self,*args, **kwargs):
        email= self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email)
        accepted_domains = ['audit.gov.gh']
        _, domain = email.split('@')

        if email:
            if email_exists.exists():
                raise forms.ValidationError({'email':["A user with this email address alread exist"]})
            elif domain.lower() not in accepted_domains:
                raise forms.ValidationError({'email':["Please enter a valid corporate emails address"]})
        return super(CreateUserForm, self).clean(*args, **kwargs)

class ProfileUserForm(forms.ModelForm):

    class Meta():
        model =models.Profile
        fields=['grade','region','district','telephone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['district'].queryset = self.instance.region.district_set.order_by('districtname')



class EditProfileUserForm(forms.ModelForm):

    class Meta():
        model =models.Profile
        fields=['grade','region','district','telephone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by('districtname')
