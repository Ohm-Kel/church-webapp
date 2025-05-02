from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import ExecutiveMember, Event, PersonalityOfTheWeek, Sermon, Member

class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Create admin user and obtain JWT token once
        self.admin = User.objects.create_superuser(
            username='testadmin', password='pass1234', email='admin@example.com'
        )
        token_url = reverse('token_obtain_pair')
        resp = self.client.post(token_url,
                                {'username': 'testadmin', 'password': 'pass1234'},
                                format='json')
        self.access_token = resp.data['access']
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

class ExecutiveMemberAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.member = ExecutiveMember.objects.create(
            name='John Doe', role='Pastor', bio='Bio', photo=''
        )
        self.url_list   = reverse('executivemember-list')
        self.url_detail = reverse('executivemember-detail', args=[self.member.id])

    def test_list(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail(self):
        resp = self.client.get(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'John Doe')

    def test_create_requires_auth(self):
        data = {'name': 'Jane Doe', 'role': 'Elder', 'bio': 'Bio', 'photo': ''}
        # Unauthenticated
        resp = self.client.post(self.url_list, data, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # Authenticated
        resp = self.client.post(self.url_list, data, format='json', **self.auth_header)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

class EventAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            title='Sample', description='Desc',
            date='2025-05-10T10:00:00Z', location='Main', image=''
        )
        self.url_list   = reverse('event-list')
        self.url_detail = reverse('event-detail', args=[self.event.id])

    def test_list_pagination(self):
        resp = self.client.get(f"{self.url_list}?page=1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_filtering(self):
        resp = self.client.get(f"{self.url_list}?location=Main")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_ordering(self):
        resp = self.client.get(f"{self.url_list}?ordering=-date")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_requires_auth(self):
        data = {'title': 'New', 'description': 'Desc',
                'date': '2025-05-11T10:00:00Z', 'location': 'Chapel', 'image': ''}
        # Unauthenticated
        unauth = self.client.post(self.url_list, data, format='json')
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # Authenticated
        auth = self.client.post(self.url_list, data, format='json', **self.auth_header)
        self.assertEqual(auth.status_code, status.HTTP_201_CREATED)

class PersonalityAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.obj = PersonalityOfTheWeek.objects.create(
            name='Alice', why_selected='Good', photo='', week_date='2025-05-01'
        )
        self.url_list   = reverse('personalityoftheweek-list')
        self.url_detail = reverse('personalityoftheweek-detail', args=[self.obj.id])

    def test_list(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_search(self):
        resp = self.client.get(f"{self.url_list}?search=Alice")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

class SermonAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.obj = Sermon.objects.create(
            title='Sermon', preacher='John', date='2025-05-01',
            media_url='http://', description='Desc'
        )
        self.url_list   = reverse('sermon-list')
        self.url_detail = reverse('sermon-detail', args=[self.obj.id])

    def test_list(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail(self):
        resp = self.client.get(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

class MemberAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.obj = Member.objects.create(
            name='Bob', gender='M', phone='1234',
            email='b@x.com', join_date='2025-05-01', status='Active'
        )
        self.url_list   = reverse('member-list')
        self.url_detail = reverse('member-detail', args=[self.obj.id])

    def test_list(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail(self):
        resp = self.client.get(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        

