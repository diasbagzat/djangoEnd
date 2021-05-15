from rest_framework import serializers
from auth_.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                address=validated_data['address'],
                phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if data['email'] == '':
            raise serializers.ValidationError("Empty email field!!!")
        return data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance
