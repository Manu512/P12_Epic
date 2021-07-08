""" serializers.py """
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            validators=[UniqueValidator(User.objects.all())]
    )
    username = serializers.EmailField(
            validators=[UniqueValidator(User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Methode qui permet de hash le mot de passe dans la base de données. Autrement il est en clair.
        """
        validated_data["password"] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def validate(self, attrs):
        """
        Methode de validation pour forcer le passage par le validator de MDP de Django
        Cela permet de respecté les préconisations OWASP via le paramétrage Django.
        :param attrs: données a valider
        :return: les paramètres validés
        """
        user = User(**attrs)

        password = attrs.get('password')

        errors = dict()
        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
            validators=[UniqueValidator(models.Client.objects.all())]
    )
    sales_contact = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = models.Client
        fields = ['id', 'url', 'company_name', 'last_name', 'first_name', 'phone', 'email',
                  'sales_contact', 'prospect']


class ContratSerializer(serializers.HyperlinkedModelSerializer):

    amount = serializers.IntegerField()
    payement_due = serializers.DateField(format="%Y-%m-%d")
    sales_contact = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    client = serializers.SlugRelatedField(queryset=models.Client.objects.all(), slug_field='company_name')

    class Meta:
        model = models.Contrat
        fields = ['url', 'sales_contact', 'client', 'status', 'amount',
                  'payement_due', 'event']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    contrat = serializers.ReadOnlyField(source='Event.client')
    support_contact = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    event_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
    class Meta:
        model = models.Event
        fields = ['url', 'client', 'contrat',  'support_contact', 'event_date', 'event_status', 'attendees', 'notes']
