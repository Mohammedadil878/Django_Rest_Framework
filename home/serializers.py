from rest_framework import serializers
from .models import Color, Person
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username is taken.')
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email is taken.')
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data) 
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name', 'id']

class PeopleSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()
    # color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        # fields = ['name', 'age', 'color']
        fields = '__all__'
        # depth = 1

    # def validate_age(self, age):
    #     print(age)
    #     return age

    # def get_color_info(self, obj):
    #     if obj.color:
    #         color_obj = Color.objects.get(id = obj.color.id)
    #         return { 'color_name' : color_obj.color_name, 'hex_code' : '#000' }
    #     else:
    #         return { 'color_name' : '', 'hex_code' : '#000' }

    def validate(self, data):
        special_cahracters = "\!@#$%^&*()-+?_<>,./|}{`~:;'[]"
        if any(c in  special_cahracters for c in data['name']):
            raise serializers.ValidationError('Name cannot contain special characters.')
        return data
        # if data.get('age') and data['age'] < 18:
        #     raise serializers.ValidationError('Age should be greater than 18.')
        
