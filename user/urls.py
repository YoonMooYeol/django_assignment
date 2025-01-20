# from django.urls import path
# from . import views


# urlpatterns = [
    
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
#     path('signup/', views.SignUpView.as_view(), name='signup'),
    
    
#     path('', views.UserListView.as_view(), name='profiles'),  # 모든프로필
#     path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),  
#     path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
#     path('profile/delete/', views.DeleteProfileView.as_view(), name='delete_profile'),
#     path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
#     path('protected/', views.MyProtectedView.as_view(), name='protected'),

# ]



from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('', views.CustomUserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', views.CustomUserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
]