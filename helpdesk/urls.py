from django.urls import path
from .import views


app_name = 'helpdesk'

urlpatterns = [
         path('', views.login_view, name="login"),
         path('logout', views.login_view, name="logout"),
         path('signup', views.signup, name="signup"),
         path('profile', views.profile, name="profile"),
         path('editprofile', views.editprofile, name="editprofile"),
         path('ajax/load-district/', views.load_district, name="ajax_load_cities"),

         path('ajax/load-agent/', views.load_agent, name="ajax_load_agent"),

         path('userdashbord/', views.user_dashboard, name="userdashboard"),
         path('Newticket/', views.user_ticket, name="userticket"),
         path('edit/<str:pk>/', views.edit_user_ticket, name="edituserticket"),
         path('ticketdetail/<str:pk>/', views.view_user_ticket, name="userticketdetails"),


         path('ticket/', views.agent_ticket, name="ticket"),
         path('editticket/<str:pk>/',views.edit_agent_ticket, name="editticket"),
         path('detail/<str:pk>/',views.detail_agent_ticket, name ="detail"),
         path('agentdashbord/', views.agent_dashboard, name="agentdashboard"),
         path('ticketescalated/', views.agent_escalated, name="ticketescalated"),
         path('escaladeticket/<str:pk>/',views.escalate_ticket,name="escaladeticket"),

         path('helpdeskdashbord/', views.helpdesk_dashboard, name="helpdeskdashboard"),
         path('edittickethelp/<str:pk>/',views.edit_heldesk_ticket, name="edittickethelp"),
         # path('helpdeskticket/<str:pk>/',views.heldesk_ticketedit, name="helpdeskticket"),


         path('close/<str:pk>/', views.closeticket, name="closeticket"),

         path('agentsearch/', views.agent_search, name="agentsearch"),
         path('search/',views.search, name="search"),
         path('dashboard/', views.dashboard, name="dashboard"),
         path('dirsearch/', views.dirsearch, name="dirsearch"),


         path('opened/', views.open_ticket, name= "open"),
         path('closed/',views.closed_ticket, name ="closed"),
         path('solved/', views.solved_ticket,name ="solved"),
         path('total/', views.total_ticket,name ="total"),

]
