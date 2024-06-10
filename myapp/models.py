from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100) 
    hourly_start_time = models.DateField(null=True ,blank=True)
    hourly_end_time = models.DateField(null=True , blank=True)
    hourly_project_limit = models.IntegerField(null=True , blank=True)
    created_at = models.DateField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.project_name}"
    
    
class Project_Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    description = models.CharField(max_length=600)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.project.project_name}"
    
class Manager(models.Model):
    name=models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='managers' , blank=True ,null=True)

    def __str__(self):
        return f"{self.name}"
    
class Project_Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
class Status(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
      return f"{self.name}"
  
class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Roles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)

    def __str__(self):
        return self.name

class UserAndRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"   
    
class Staff(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    designation = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    
class Employee(models.Model):
    name=models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='employee' , blank=True ,null=True)

    def __str__(self):
        return f"{self.name}"
    
class TeamLead(models.Model):
    name=models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='team_lead' , blank=True ,null=True)

    def __str__(self):
        return f"{self.name}"