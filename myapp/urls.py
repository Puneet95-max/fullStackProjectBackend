from django.urls import path
from .views import ProjectDetails , ProjectMilstoneDetails  , ProjectTypeDetails  , StatusType  ,login , RolesDetials , UserAndRolesDetails , StaffDetails , ManagerDetails , projectAPI , daily_report_list , report_view , user_roles_view , create_role , update_role

urlpatterns = [
    path('details/', ProjectDetails, name='projectDetails'),
    path('test/', ProjectMilstoneDetails, name='projectDetails'),
    path('project-type/', ProjectTypeDetails, name='ProjectTypeDetails'),
    path('status-type/', StatusType, name='StatusType'),
    path('login/', login , name='login') , 
    path('roles/', RolesDetials , name='RolesDetials'),
    path('user-roles/', UserAndRolesDetails , name='UserAndRolesDetails'),
    path('staff/', StaffDetails , name='StaffDetails') ,
    path('staff/<int:pk>/', StaffDetails, name='staff-detail'),
    path('manager-details/', ManagerDetails , name='ManagerDetails'),    
    path('project/<int:pk>/', projectAPI, name='ProjectAPI'),
    path('report/', daily_report_list, name='daily_report_list'),
    path('report/<int:id>/', report_view, name='report_view'),
    path('roles/<int:user_id>/', user_roles_view ,  name='user_roles_view'),
    path('create-role/', create_role, name='create_role'),
    path('update-role/<int:pk>/', update_role, name='update_role'),
]