from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 
                 'profile_image', 'bio')

class CustomUserChangeForm(UserChangeForm):
    password = None  
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'profile_image', 'bio')
