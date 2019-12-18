from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

from invitation.models import Invitation


class InvitationAPITest(TestCase):

    def setUp(self):
        self.dummy_data1 = {'email': 'invitation_email@gmail.com'}
        self.dummy_data2 = {'email': 'patched_email@gmail.com'}
        self.client = APIClient()
        self.temp_user = User.objects.create(
            email='test@test.com', username='test_user', password='password123')
        self.client.force_login(self.temp_user)

    def test_create_invitation(self):
        res = self.client.post('/api/invitations/',
                               self.dummy_data1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invitation.objects.count(), 1)

    def test_view_invitations(self):
        res = self.client.post('/api/invitations/',
                               self.dummy_data1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get('/api/invitations/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data.get('results')), 1)

    def test_patch_invitation(self):
        res = self.client.post('/api/invitations/',
                               self.dummy_data1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        invitation_id = str(Invitation.objects.get().id)
        res = self.client.patch(
            '/api/invitations/{id}/'.format(id=invitation_id),
            self.dummy_data2, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.dummy_data2['email'])

    def test_delete_invitation(self):
        res = self.client.post('/api/invitations/',
                               self.dummy_data1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        invitation_id = str(Invitation.objects.get().id)
        res = self.client.delete(
            '/api/invitations/{id}/'.format(id=invitation_id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invitation.objects.count(), 0)
