from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from .models import  Project , Project_Milestone , Status , Project_Type   , Roles , UserAndRoles , Staff  , Manager   , DailyReport
from .serializers import  ProjectSerializer  , Project_MilestoneSerializer , ProjectTypeSerializer , StatusSerializer   , RoleSerializer , UserAndRolesSerializer , StaffSerializer  , ManagerSerializer , DailyReportCreateSerializer , DailyReportGetSerializer , UserRoleAssignmentSerializer , RoleCreateUpdateSerializer
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User  # Import the User model if not already imported
from django.core.exceptions import ObjectDoesNotExist  #
from django.views.decorators.csrf  import csrf_protect
from django.utils.decorators import method_decorator

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['GET', 'POST'])
def ProjectDetails(request):
    if request.method == 'GET':
        items = Project.objects.all()
        serializer = ProjectSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Project has been added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def projectAPI(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Project has been updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response({"message": "Project has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def ProjectMilstoneDetails(request):
    if request.method == 'GET':
        items = Project_Milestone.objects.all()
        serializer = Project_MilestoneSerializer(items, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def ProjectTypeDetails(request):
    if request.method == 'GET':
        items = Project_Type.objects.all()
        serializer = ProjectTypeSerializer(items, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def StatusType(request):
    if request.method == 'GET':
        items = Status.objects.all()
        serializer = StatusSerializer(items, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    user_data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
    }

    try:
        user_and_roles = UserAndRoles.objects.filter(user=user)
        for user_role in user_and_roles:
           if user_role.user.id == user_data['id']:
            role_data = {
                'id': user_role.role.id,
                'name': user_role.role.name,
                'permissions': [{'action': perm.action, 'subject': perm.subject} for perm in user_role.role.permissions.all()]  # Fetch related permissions
            }
            user_data['role'] = role_data
            break 
    except ObjectDoesNotExist:
        user_data['role'] = None 

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    response_data = {
        'token': token,
        'user': user_data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def RolesDetials(request):
    if request.method == 'GET':
        items = Roles.objects.all()
        serializer = RoleSerializer(items, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def create_role(request):
    if request.method == 'POST':
        serializer = RoleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_role(request, pk):
    try:
        role = Roles.objects.get(pk=pk)
    except Roles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = RoleCreateUpdateSerializer(role, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def UserAndRolesDetails(request):
    if request.method == 'GET':
        items = UserAndRoles.objects.all()
        serializer = UserAndRolesSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserRoleAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            user_role = serializer.save()
            serialized_user_role = UserAndRolesSerializer(user_role)
            return Response(serialized_user_role.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def StaffDetails(request, pk=None):
    if request.method == 'GET':
        # GET all staff or single staff if pk is provided
        if pk:
            try:
                staff = Staff.objects.get(pk=pk)
                serializer = StaffSerializer(staff)
                return Response(serializer.data)
            except Staff.DoesNotExist:
                return Response({"message": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Staff.objects.all()
            serializer = StaffSerializer(items, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        # POST method to add new staff
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Staff has been added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        # PUT method to update existing staff
        if pk:
            try:
                staff = Staff.objects.get(pk=pk)
                serializer = StaffSerializer(staff, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Staff.DoesNotExist:
                return Response({"message": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Provide a valid staff ID"}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # DELETE method to delete staff
        if pk:
            try:
                staff = Staff.objects.get(pk=pk)
                staff.delete()
                return Response({"message": "Staff has been deleted"}, status=status.HTTP_204_NO_CONTENT)
            except Staff.DoesNotExist:
                return Response({"message": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Provide a valid staff ID"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def ManagerDetails(request):
    if request.method == 'GET':
        items = Manager.objects.all()
        serializer = ManagerSerializer(items, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def daily_report_list(request):
    reports = DailyReport.objects.all()
    serializer = DailyReportGetSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def report_view(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        tasks = request.data.get('tasks')
    
        if not tasks:
            return Response({'error': 'No tasks provided'}, status=status.HTTP_400_BAD_REQUEST)
    
        for task_data in tasks:
            task_data['user'] = user.id
            serializer = DailyReportCreateSerializer(data=task_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'message': 'Tasks saved successfully'}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        reports = DailyReport.objects.filter(user=user)
        serializer = DailyReportGetSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def user_roles_view(request, user_id):
    user_roles = UserAndRoles.objects.filter(user_id=user_id)
    if not user_roles.exists():
        return Response({"detail": "User not found or no roles assigned"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserAndRolesSerializer(user_roles, many=True)
    user_role_data = serializer.data
    
    if user_role_data:
        # Assuming you always want the first role in the list
        response_data = user_role_data[0]
    else:
        response_data = {}

    return Response(response_data, status=status.HTTP_200_OK)