from django.contrib import admin
from helpdesk.models import Profile,Grade,Region,District,Ticket,Status, agent_Status,Technician,Team,Ticket_Comments,AssignedTicket,Prority

# Register your models here.
admin.site.register(Profile)
admin.site.register(Grade)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Ticket)
admin.site.register(Status)
admin.site.register(agent_Status)
admin.site.register(Technician)
admin.site.register(Team)
admin.site.register(Ticket_Comments)
admin.site.register(AssignedTicket)
admin.site.register(Prority)
