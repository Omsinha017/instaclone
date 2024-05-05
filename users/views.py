from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer, NetworkEdgeCreationSerializer, NetworkEdgeViewSerializer
from .models import UserProfile, NetworkEdge

@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    response_data = {
        "errors": None,
        "data": None
    }
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data["data"] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        response_status = status.HTTP_201_CREATED
    else:
        response_data["errors"] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = UserProfile.objects.all()
    serializer = UserProfileViewSerializer(instance=users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileDetail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        user = UserProfile.objects.filter(id=pk).first()
        if user:
            serializer = UserProfileViewSerializer(instance=user)
            response_data = {
                "data" : serializer.data,
                "errors": None
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "data" : None,
                "errors": "User Does Not Exist"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, pk):
        user_profile_serializer = UserProfileUpdateSerializer(instance=request.user.profile,
                                                        data=request.data)
        if user_profile_serializer.is_valid():
            user_profile = user_profile_serializer.save()

            response_data = {
                "data": UserProfileViewSerializer(instance=user_profile).data,
                "errors": None
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "data": None,
                "errors": user_profile_serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        user = request.user
        user.delete()

        response_data = {
            "data": None,
            "message": "User Successfully Deleted"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class UserNetworkEdge(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      generics.GenericAPIView):

    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NetworkEdgeViewSerializer
        return self.serializer_class
    
    def get_queryset(self):
        edge_direction = self.request['direction']
        if edge_direction == "followers":
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == "following":
            return self.queryset.filter(from_user=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request['from_user'] = request.user.profile.id
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile,
                                                  to_user=request.data['from_user'])

        if network_edge.exists():
            network_edge.delete()
            message = "User unfollowed"
        else:
            message = "User Does Not exist"
        return Response({'data': None, 'message': message}, status=status.HTTP_200_OK)
