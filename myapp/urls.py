from django.urls import path
from .views import ProjectDetails , ProjectMilstoneDetails  , ProjectTypeDetails  , StatusType , MangerDetials ,login , RolesDetials , UserAndRolesDetails , StaffDetails

urlpatterns = [
    path('details/', ProjectDetails, name='projectDetails'),
    path('test/', ProjectMilstoneDetails, name='projectDetails'),
    path('project-type/', ProjectTypeDetails, name='ProjectTypeDetails'),
    path('status-type/', StatusType, name='StatusType'),
    path('manager-details/',MangerDetials , name='MangerDetials'),
    path('login/', login , name='login') , 
    path('roles/', RolesDetials , name='RolesDetials'),
    path('user-roles/', UserAndRolesDetails , name='UserAndRolesDetails'),
    path('staff/', StaffDetails , name='StaffDetails')   
]