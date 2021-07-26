# from django.test import TestCase
# from pytest_django.asserts import assertTemplateUsed
# from user.models import User
#
# # Create your tests here.
#
# class ListClientsTest(TestCase):
#
#     def test_u(self):
#
#         user = User.objects.get(username='c_manu')
#         self.client.force_authenticate(user=user)
#         url = 'http://127.0.0.1:8000/api/client/'
#         response = self.client.get(path=url)
#         self.assertEqual(response.status_code, 200)
#
#
#
#
# def test_an_admin_view(admin_client):
#     response = admin_client.get('/admin/')
#     assert response.status_code == 200
#
#
# def test_api_client_list(admin_client):
#     response = admin_client.get('/api/client/')
#     assert response.status_code == 200
#
#
# def test_api_client_detail(admin_client):
#     response = admin_client.get('/api/client/1/')
#     assert response.status_code == 200
#
#
# def test_api_client_contrat_list(admin_client):
#     response = admin_client.get('/api/client/1/contrat/')
#     assert response.status_code == 200
#
#
# def test_api_client_contrat_detail(admin_client):
#     response = admin_client.get('/api/client/1/contrat/1/')
#     assert response.status_code == 200
#
#
# def test_api_event_list(admin_client):
#     response = admin_client.get('/api/client/1/contrat/1/event/')
#     assert response.status_code == 200
#
#
# def test_api_event_detail(admin_client):
#     response = admin_client.get('/api/client/1/contrat/1/event/1/')
#     assert response.status_code == 200
