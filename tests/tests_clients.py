import json

import pytest
from django.test import Client

from api.models import Client as Clt
from user.models import User

pytestmark = pytest.mark.django_db

endpoints = ["client", "contrat", "event"]
endpoints_details = ["client/1/", "contrat/1/"]


@pytest.mark.django_db
class TestUsers:
    pytestmark = pytest.mark.django_db
    client = Client()

    def test_admin(self):
        me = User.objects.get(username='admin')
        assert me.is_superuser

    def test_commercial1(self):
        me = User.objects.get(username='commercial1')
        assert not me.is_superuser
        assert me.is_vendor()

    def test_commercial2(self):
        me = User.objects.get(username='commercial1')
        assert not me.is_superuser
        assert me.is_vendor()

    def test_support1(self):
        me = User.objects.get(username='support1')
        assert not me.is_superuser
        assert me.is_support()

    def test_support2(self):
        me = User.objects.get(username='support2')
        assert not me.is_superuser
        assert me.is_support()

    def test_gestion(self):
        me = User.objects.get(username='management')
        assert not me.is_superuser
        assert me.is_management()

    def test_unauthenticated_client(self):
        response = self.client.get('/administration/')
        print(response.content)
        assert response.status_code == 302

    def test_authenticated_admin(self):
        username = "admin"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_authenticated_management(self):
        username = "management"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_authenticated_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_authenticated_commercial2(self):
        username = "commercial2"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_authenticated_support(self):
        username = "support1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_authenticated_support2(self):
        username = "support2"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/administration/')
        assert b"Site d\xe2\x80\x99administration | EPIC Event" in response.content
        assert response.status_code == 200

    def test_client_1(self):
        me = Clt.objects.get(pk=1)
        assert me.company_name == 'Finance'
        assert me.prospect
        assert User.objects.get(id=me.sales_contact_id).team == 'Equipe commerciale'

    def test_client_2(self):
        me = Clt.objects.get(pk=2)
        assert me.company_name == "Caisse Primaire d'Assurance Maladie"
        assert me.prospect
        assert User.objects.get(id=me.sales_contact_id).team == 'Equipe commerciale'

    def test_client_3(self):
        me = Clt.objects.get(pk=3)
        assert me.company_name == "En Plaine Air"
        assert not me.prospect
        assert User.objects.get(id=me.sales_contact_id).team == 'Equipe commerciale'

    def test_client_4(self):
        me = Clt.objects.get(pk=4)
        assert me.company_name == "Ordre des Medecins"
        assert me.prospect
        assert User.objects.get(id=me.sales_contact_id).team == 'Equipe commerciale'

    def test_client_5(self):
        me = Clt.objects.get(pk=5)
        assert me.company_name == 'On va sortir'
        assert me.prospect
        assert User.objects.get(id=me.sales_contact_id).team == 'Equipe commerciale'


class TestAPI:
    pytestmark = pytest.mark.django_db
    client = Client()

    def test_authenticated_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/api/client/')
        json_data = json.loads(response.content)
        assert len(json_data['results']) == 5
        assert response.status_code == 200

    def test_list_all_endpoint_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        for endpoint in endpoints:
            response = self.client.get('/api/' + endpoint + '/')
            assert response.status_code == 200

        for endpoint in endpoints_details:
            response = self.client.get('/api/' + endpoint)
            assert response.status_code == 200

    def test_list_all_endpoint_commercial2(self):
        username = "commercial2"
        password = "1234"
        self.client.login(username=username, password=password)
        for endpoint in endpoints:
            response = self.client.get('/api/' + endpoint + '/')
            assert response.status_code == 200

        for endpoint in endpoints_details:
            response = self.client.get('/api/' + endpoint)
            assert response.status_code == 200

    def test_list_all_endpoint_support1(self):
        username = "support1"
        password = "1234"
        self.client.login(username=username, password=password)
        for endpoint in endpoints:
            response = self.client.get('/api/' + endpoint + '/')
            assert response.status_code == 200

        for endpoint in endpoints_details:
            response = self.client.get('/api/' + endpoint)
            assert response.status_code == 200

    def test_list_all_endpoint_support2(self):
        username = "support2"
        password = "1234"
        self.client.login(username=username, password=password)
        for endpoint in endpoints:
            response = self.client.get('/api/' + endpoint + '/')
            assert response.status_code == 200

        for endpoint in endpoints_details:
            response = self.client.get('/api/' + endpoint)
            assert response.status_code == 200

    def test_list_all_endpoint_management(self):
        username = "management"
        password = "1234"
        self.client.login(username=username, password=password)
        for endpoint in endpoints:
            response = self.client.get('/api/' + endpoint + '/')
            assert response.status_code == 200

        for endpoint in endpoints_details:
            response = self.client.get('/api/' + endpoint)
            assert response.status_code == 200

    def test_delete_client1_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.delete('/api/client/1/')
        assert response.status_code == 403

    def test_delete_client1_management(self):
        username = "management"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.delete('/api/client/1/')
        assert response.status_code == 403

    def test_search_client_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/api/client/?client=WALDNER')
        assert response.status_code == 200

    def test_search_email_commercial1(self):
        username = "commercial1"
        password = "1234"
        self.client.login(username=username, password=password)
        response = self.client.get('/api/client/?email=Schmidt@ODM.fr')
        assert response.status_code == 200
