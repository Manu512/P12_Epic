""" serializers.py """
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import User
from . import models
from .models import Client, Contrat, Event


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
    sales_contact = serializers.StringRelatedField(many=False)
    date_updated = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)
    prospect = serializers.BooleanField(default=True)

    def create(self, validated_data):
        validated_data['sales_contact'] = self.context['request'].user
        new_client = Client.objects.create(**validated_data)
        new_client.save()
        return new_client

    class Meta:
        model = models.Client
        fields = ['id', 'url', 'company_name', 'last_name', 'first_name', 'phone', 'email',
                  'sales_contact', 'prospect', 'date_created', 'date_updated']
        # read_only_fields = ['sales_contact']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'sales_contact': {'read_only': True},
        }


class ContratSerializer(serializers.HyperlinkedModelSerializer):
    amount = serializers.IntegerField()
    payement_due = serializers.DateField(format="%Y-%m-%d")
    sales_contact = serializers.StringRelatedField(many=False)
    client = serializers.SlugRelatedField(queryset=models.Client.objects.all(), slug_field='company_name')
    date_updated = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)

    def create(self, validated_data):
        validated_data['sales_contact'] = self.context['request'].user
        new_contrat = Contrat.objects.create(**validated_data)
        new_contrat.save()
        return new_contrat

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
            if validated_data['status']:
                self.instance.client.prospect = False
                self.instance = self.update(self.instance, validated_data)
                Client.objects.filter(id=self.instance.client_id).update(prospect=False)
                event_exist = Event.objects.filter(contrat_id=self.instance.pk).exists()
                if not event_exist:
                    Event.objects.create(contrat_id=self.instance.pk, client=validated_data['client'])
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )
            if validated_data['status']:
                Event.objects.create(contrat_id=self.instance.pk, client=validated_data['client'])
                Client.objects.filter(id=self.instance.client_id).update(prospect=False)

        return self.instance

    class Meta:
        model = models.Contrat
        fields = ['url', 'sales_contact', 'client', 'status', 'amount',
                  'payement_due', 'date_created', 'date_updated']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'sales_contact': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):
    contrat = serializers.StringRelatedField(many=False)
    sales_contact = serializers.StringRelatedField(many=False)
    client = serializers.StringRelatedField(many=False)
    event_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")
    date_updated = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", read_only=True)

    class Meta:
        model = models.Event
        fields = ['contrat', 'url', 'client', 'sales_contact', 'support_contact', 'event_date', 'event_status',
                  'attendees', 'notes', 'date_created', 'date_updated']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
            'support_contact': {'read_only': True},
        }
