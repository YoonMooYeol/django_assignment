from rest_framework import serializers
from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'profile_image', 'bio', 'author')
        
        
class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = CustomUser
        fields = ('email','password', 'profile_image', 'bio', 'author')




