from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}
    
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'Error: That username is taken.'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'Error: That email in being used by an existing account.'})
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'Error: Passwords do not match.'})
        
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        return account        

class PasswordChangeSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['current_password', 'new_password']
    
    def save(self):
        account = self.context['request'].user
        current_password = self.validated_data['current_password']
        new_password = self.validated_data['new_password']
        
        if not account.check_password(current_password):
            raise serializers.ValidationError({'Error: This isn\'t the current password.'})
        
        if current_password == new_password:
            raise serializers.ValidationError({'Error: New password should be different from current one.'})
        
        account.set_password(new_password)
        account.save()
        return account

class ProfileSerializer(serializers.ModelSerializer):
    user_quotes = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'user_quotes']