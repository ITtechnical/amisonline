from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from .models import Profile,UserSession
from django.shortcuts import redirect
from amis.settings import EMAIL_HOST_USER
from django.core.mail import send_mail,EmailMessage
from .import models
from django.contrib.sessions.models import Session
from .import views


def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='staff')
		instance.groups.add(group)
		Profile.objects.create(
			user=instance,
			name=instance.first_name +" "+ instance.last_name,
			email =instance.email,
			is_staff = True,
			is_new =True
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)


@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()


    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
	)
    return redirect('helpdesk:login')
