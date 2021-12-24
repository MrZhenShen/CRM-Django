from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_409_CONFLICT
from .models import Client, Good, Status, Project
from datetime import datetime

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'telephone_number',
            'email',
            'username',
            'password',
            'is_staff',
            'company_name',
            'company_link',
            'industry',
            'role',
            'country',
            'city',
            'last_login',
            'date_joined'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        client = Client(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            telephone_number = validated_data['telephone_number'],
            email=validated_data['email'],
            is_staff = False,
            company_name = validated_data['company_name'],
            industry = validated_data['industry'],
            last_login = datetime.now(),
            username = validated_data['username']
        )

        users = Client.objects.filter(email=client.email)
        if users:
            raise serializers.ValidationError({'Email '+client.email+" already exists"})

        client.set_password(validated_data['password'])
        client.save()
        Token.objects.create(user=client)
        return client


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = [
            'id',
            'name',
            'description',
            'example_image',
            'pricing'
        ]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'title',
            'color'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    Good = GoodSerializer()
    Client = ClientSerializer()
    Status = StatusSerializer()

    class Meta:
        model = Project
        fields = [
            'id',
            'Good',
            'Client',
            'client_comment',
            'Status'
        ]