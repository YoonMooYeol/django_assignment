# from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.views import LoginView, LogoutView
# from django.views.generic import ListView, CreateView, UpdateView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView

# from .models import CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm


# class MyProtectedView(LoginRequiredMixin, TemplateView):
#     template_name = 'user/login.html'
#     login_url = '/login/'  
#     redirect_field_name = 'next' 


# class UserListView(ListView):
#     model = CustomUser
#     template_name = 'user/profiles.html'
#     context_object_name = 'users'


# class CustomLoginView(LoginView):
#     template_name = 'user/login.html'
#     success_url = reverse_lazy('profiles')  # namespace 추가

#     def get_success_url(self):
#         return self.success_url


# class CustomLogoutView(LoginRequiredMixin,LogoutView):
#     next_page = 'login'  # namespace 추가

# class SignUpView(CreateView):
#     model = CustomUser
#     form_class = CustomUserCreationForm
#     template_name = 'user/signup.html'
#     success_url = reverse_lazy('profiles')  # namespace 추가
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, '회원가입이 완료되었습니다.')
#         return response


# class ProfileView(LoginRequiredMixin, DetailView):
#     model = CustomUser
#     template_name = 'user/profile.html'
#     context_object_name = 'user'
    
#     # 로그인하지 않은 경우 리다이렉션 설정
#     login_url = 'login'  # name='login'으로 설정된 URL 네임

#     def get_object(self, queryset=None):
#         pk = self.kwargs.get('pk')
#         if pk:
#             return get_object_or_404(CustomUser, pk=pk)
#         return self.request.user

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         context['followers_count'] = user.followers.count()
#         context['following_count'] = user.followings.count()
#         return context

# class UpdateProfileView(LoginRequiredMixin, UpdateView):
#     model = CustomUser
#     form_class = CustomUserChangeForm
#     template_name = 'user/updateprofile.html'
    
#     def get_object(self, queryset=None):
#         return self.request.user
    
#     def get_success_url(self):
#         return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
    
#     def form_valid(self, form):
#         messages.success(self.request, '프로필이 수정되었습니다.')
#         return super().form_valid(form)



# class DeleteProfileView(LoginRequiredMixin, DetailView):
#     model = CustomUser
    
#     def get_object(self, queryset=None):
#         return self.request.user
    
#     def post(self, request, *args, **kwargs):
#         user = self.request.user
#         user.delete()
#         messages.success(self.request, '회원탈퇴가 완료되었습니다.')
#         return redirect('login')



# @login_required
# @require_POST
# def follow_toggle(request, user_id):
#     follow_user = get_object_or_404(CustomUser, pk=user_id)
#     user = request.user
    
#     if user.followings.filter(id=follow_user.id).exists():
#         user.followings.remove(follow_user)
#         is_following = False
#     else:
#         user.followings.add(follow_user)
#         is_following = True
    
#     return redirect('profile', follow_user.pk) 


# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import UserSerializer, CustomTokenObtainPairSerializer

# class SignUpView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
    
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import CustomUser
from user.serializers import UserSerializer, UserUserRetrieveUpdateDestroySerializer
from django_assignment.permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    

class CustomUserListCreateView(APIView):
    
    def get_permissions(self):
        return [AllowAny()]
    
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.is_active = True
                user.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



    

class CustomUserRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "사용자를 찾을 수 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            # 권한 체크
            if user.id != request.user.id:
                return Response(
                    {"error": "본인의 프로필만 수정할 수 있습니다."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            serializer = UserUserRetrieveUpdateDestroySerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "사용자를 찾을 수 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            # 권한 체크
            if user.id != request.user.id:
                return Response(
                    {"error": "본인의 계정만 삭제할 수 있습니다."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "사용자를 찾을 수 없습니다."}, 
                status=status.HTTP_404_NOT_FOUND
            )