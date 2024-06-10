from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status
from .models import  Project , Project_Milestone , Status , Project_Type , Manager  , Roles , UserAndRoles , Staff
from .serializers import  ProjectSerializer  , Project_MilestoneSerializer , ProjectTypeSerializer , StatusSerializer , ManagerSerializer  , RoleSerializer , UserAndRolesSerializer , StaffSerializer
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User  # Import the User model if not already imported
from django.core.exceptions import ObjectDoesNotExist  #

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
    
@api_view(['GET'])
def MangerDetials(request):
    if request.method == 'GET':
        items = Manager.objects.all()
        serializer = ManagerSerializer(items, many=True)
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
                'permissions': [{'name': perm.name, 'codename': perm.codename} for perm in user_role.role.permissions.all()]  # Fetch related permissions
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
    
@api_view(['GET'])
def  UserAndRolesDetails(request):
    if request.method == 'GET':
        items = UserAndRoles.objects.all()
        serializer = UserAndRolesSerializer(items, many=True)
        return Response(serializer.data)
    
@api_view(['GET' , 'POST'])
def StaffDetails(request):
    if request.method == 'GET':
        items = Staff.objects.all()
        serializer = StaffSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Staff has been added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
