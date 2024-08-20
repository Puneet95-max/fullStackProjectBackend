from rest_framework import serializers
from .models import Project, Project_Milestone  , Project_Type , Status  , Permission , Roles   , UserAndRoles ,  Staff  , Employee , TeamLead , Manager , DailyReport
from django.contrib.auth.models import  User

class Project_MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Milestone
        fields = ['id', 'description',  'start_date', 'end_date', 'status']
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'name']
        
    
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']

class TeamLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLead
        fields = ['id', 'name']
        

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
            Manager.objects.create(project=project, **manager_data)
            
        for milestone_data in milestones_data:
            Project_Milestone.objects.create(project=project, **milestone_data)
        
        for employee_data  in employees_data:
            Employee.objects.create(project=project, **employee_data)
        
        for teamlead_data  in team_lead_data:
            TeamLead.objects.create(project=project, **teamlead_data)
            
        return project

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop('milestones')
        managers_data = validated_data.pop('managers')
        employees_data = validated_data.pop('employee')
        team_lead_data = validated_data.pop('team_lead')

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.project_type = validated_data.get('project_type', instance.project_type)
        instance.hourly_project_limit = validated_data.get('hourly_project_limit', instance.hourly_project_limit)
        instance.hourly_end_time = validated_data.get('hourly_end_time', instance.hourly_end_time)
        instance.hourly_start_time = validated_data.get('hourly_start_time', instance.hourly_start_time)
        instance.save()

        # Update or create managers
        instance.managers.all().delete()
        for manager_data in managers_data:
            Manager.objects.create(project=instance, **manager_data)

        # Update or create milestones
        instance.milestones.all().delete()
        for milestone_data in milestones_data:
            Project_Milestone.objects.create(project=instance, **milestone_data)

        # Update or create employees
        instance.employee.all().delete()
        for employee_data in employees_data:
            Employee.objects.create(project=instance, **employee_data)

        # Update or create team leads
        instance.team_lead.all().delete()
        for teamlead_data in team_lead_data:
            TeamLead.objects.create(project=instance, **teamlead_data)

        return instance
    
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
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions']
        
class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions')
        role = Roles.objects.create(**validated_data)
        for permission_data in permissions_data:
            permission, created = Permission.objects.get_or_create(**permission_data)
            role.permissions.add(permission)
        return role

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if permissions_data is not None:
            instance.permissions.clear()
            for permission_data in permissions_data:
                permission, created = Permission.objects.get_or_create(**permission_data)
                instance.permissions.add(permission)

        return instance

            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserAndRolesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    role = RoleSerializer()

    class Meta:
        model = UserAndRoles
        fields = ('user_id', 'role')
        
class UserRoleAssignmentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        role_name = validated_data['role']

        # Check if user with this email already exists
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError("User with this email already exists.")

        # Create the user
        user = User.objects.create(username=email, email=email)
        user.set_password(password)
        user.save()

        # Create or retrieve the role
        role, created = Roles.objects.get_or_create(name=role_name)

        # Create the user role assignment
        user_role, created = UserAndRoles.objects.get_or_create(user=user, role=role)
        
        return user_role
    
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'designation', 'position']
        
class DailyReportGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DailyReport
        fields = '__all__'

class DailyReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = '__all__'
