from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Education, Experience, Resume, Skill


class ResumeFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='StrongPass123')

    def test_resume_list_requires_login(self):
        response = self.client.get(reverse('resume_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_user_can_create_resume_with_sections(self):
        self.client.login(username='tester', password='StrongPass123')

        response = self.client.post(reverse('resume_create'), {
            'template': '',
            'title': 'Frontend CV',
            'full_name': 'Олена Коваль',
            'job_title': 'Frontend Developer',
            'email': 'olena@example.com',
            'phone': '+380 00 000 00 00',
            'location': 'Київ',
            'website': 'https://example.com',
            'summary': 'Створюю зручні інтерфейси.',
            'experience-TOTAL_FORMS': '1',
            'experience-INITIAL_FORMS': '0',
            'experience-MIN_NUM_FORMS': '0',
            'experience-MAX_NUM_FORMS': '1000',
            'experience-0-company': 'Acme',
            'experience-0-position': 'Developer',
            'experience-0-start_date': '2023',
            'experience-0-end_date': '',
            'experience-0-description': 'Розробка UI.',
            'education-TOTAL_FORMS': '1',
            'education-INITIAL_FORMS': '0',
            'education-MIN_NUM_FORMS': '0',
            'education-MAX_NUM_FORMS': '1000',
            'education-0-institution': 'KPI',
            'education-0-degree': 'Computer Science',
            'education-0-start_date': '2019',
            'education-0-end_date': '2023',
            'education-0-description': '',
            'skills-TOTAL_FORMS': '2',
            'skills-INITIAL_FORMS': '0',
            'skills-MIN_NUM_FORMS': '0',
            'skills-MAX_NUM_FORMS': '1000',
            'skills-0-name': 'Django',
            'skills-0-level': 'Intermediate',
            'skills-1-name': '',
            'skills-1-level': '',
        })

        resume = Resume.objects.get()
        self.assertRedirects(response, reverse('resume_detail', args=[resume.pk]))
        self.assertEqual(resume.user, self.user)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(Skill.objects.count(), 1)

# Create your tests here.
