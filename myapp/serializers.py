from rest_framework import serializers
from .models import Project, Project_Milestone , Manager , Project_Type , Status  , Permission , Roles   , UserAndRoles ,  Staff  , Employee , TeamLead
from django.contrib.auth.models import  User

class Project_MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Milestone
        fields = ['id', 'description',  'start_date', 'end_date', 'status']
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'name']
        
    def create(self, validated_data):
        return Manager.objects.create(**validated_data)
    
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']
        
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

class TeamLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLead
        fields = ['id', 'name']
        
    def create(self, validated_data):
        return TeamLead.objects.create(**validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    milestones = Project_MilestoneSerializer(many=True)
    managers = ManagerSerializer(many=True)
    employee = EmployeeSerializer(many=True)
    team_lead = TeamLeadSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_name', 'project_type',   'milestones', 'hourly_project_limit', 'hourly_end_time', 'hourly_start_time' , 'managers'  ,  'created_at', 'employee' , 'team_lead']

    
    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones')
        managers_data = validated_data.pop('managers')
        employees_data = validated_data.pop('employee')
        team_lead_data = validated_data.pop('team_lead')

        project = Project.objects.create(**validated_data)

        for manager_data in managers_data:
            try:
                manager, created = Manager.objects.get_or_create(**manager_data)
                if not created:
                    # Handle the case where multiple objects are returned
                    manager = Manager.objects.filter(**manager_data).first()
            except Manager.MultipleObjectsReturned:
                manager = Manager.objects.filter(**manager_data).first()
            project.managers.add(manager)

        for milestone_data in milestones_data:
            Project_Milestone.objects.create(project=project, **milestone_data)
            
        for employee_data in employees_data:
            try:
                employee, created = Employee.objects.get_or_create(**employee_data)
                if not created:
                    employee = Employee.objects.filter(**employee_data).first()
            except Employee.MultipleObjectsReturned:
                employee = Employee.objects.filter(**employee_data).first()
            project.employee.add(employee)
            
        for team_lead_data in team_lead_data:
            try:
                team_lead, created = TeamLead.objects.get_or_create(**team_lead_data)
                if not created:
                    team_lead = TeamLead.objects.filter(**team_lead_data).first()
            except TeamLead.MultipleObjectsReturned:
                team_lead = TeamLead.objects.filter(**team_lead_data).first()
            project.team_lead.add(team_lead)


        return project
    
class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Type
        fields = ['id', 'name']
        
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name', 'codename')

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Roles
        fields = ('id', 'name', 'permissions')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        

class UserAndRolesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    role = RoleSerializer()

    class Meta:
        model = UserAndRoles
        fields = ('user_id', 'role')
        
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'designation', 'position']