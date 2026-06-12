from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Announcement, Education, Experience, Resume, Skill, Template


class ResumeProjectTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='StrongPass123',
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='StrongPass123',
        )

    def build_resume_payload(self, **overrides):
        payload = {
            'template': '',
            'title': 'Frontend CV',
            'full_name': 'Olena Koval',
            'job_title': 'Frontend Developer',
            'email': 'olena@example.com',
            'phone': '+380 00 000 00 00',
            'location': 'Kyiv',
            'website': 'https://example.com',
            'summary': 'I build convenient interfaces.',
            'experience-TOTAL_FORMS': '1',
            'experience-INITIAL_FORMS': '0',
            'experience-MIN_NUM_FORMS': '0',
            'experience-MAX_NUM_FORMS': '1000',
            'experience-0-company': 'Acme',
            'experience-0-position': 'Developer',
            'experience-0-start_date': '2023',
            'experience-0-end_date': '',
            'experience-0-description': 'Built UI features.',
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
        }
        payload.update(overrides)
        return payload

    def create_resume(self, user=None, **fields):
        data = {
            'user': user or self.user,
            'title': 'Backend CV',
            'full_name': 'Ivan Petrenko',
            'email': 'ivan@example.com',
        }
        data.update(fields)
        return Resume.objects.create(**data)

    def test_models_return_readable_names(self):
        resume = self.create_resume(title='Python CV')
        education = Education.objects.create(resume=resume, institution='KPI')
        experience = Experience.objects.create(
            resume=resume,
            company='Acme',
            position='Developer',
        )
        skill = Skill.objects.create(resume=resume, name='Django')
        template = Template.objects.create(name='Classic')
        announcement = Announcement.objects.create(title='News', body='Body')

        self.assertEqual(str(resume), 'Python CV')
        self.assertEqual(str(education), 'KPI')
        self.assertEqual(str(experience), 'Acme')
        self.assertEqual(str(skill), 'Django')
        self.assertEqual(str(template), 'Classic')
        self.assertEqual(str(announcement), 'News')

    def test_home_page_shows_only_active_templates_and_published_announcements(self):
        active_template = Template.objects.create(name='Active', is_active=True)
        Template.objects.create(name='Hidden', is_active=False)
        published = Announcement.objects.create(title='Published', body='Visible')
        Announcement.objects.create(title='Draft', body='Hidden', is_published=False)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(active_template, response.context['templates'])
        self.assertNotContains(response, 'Hidden')
        self.assertIn(published, response.context['announcements'])
        self.assertNotContains(response, 'Draft')

    def test_resume_list_requires_login(self):
        response = self.client.get(reverse('resume_list'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("resume_list")}',
        )

    def test_resume_list_shows_only_current_user_resumes(self):
        own_resume = self.create_resume(title='My Resume')
        self.create_resume(user=self.other_user, title='Other Resume')
        self.client.login(username='tester', password='StrongPass123')

        response = self.client.get(reverse('resume_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_resume.title)
        self.assertNotContains(response, 'Other Resume')

    def test_user_can_create_resume_with_sections(self):
        self.client.login(username='tester', password='StrongPass123')

        response = self.client.post(
            reverse('resume_create'),
            self.build_resume_payload(),
        )

        resume = Resume.objects.get()
        self.assertRedirects(response, reverse('resume_detail', args=[resume.pk]))
        self.assertEqual(resume.user, self.user)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(Skill.objects.count(), 1)

    def test_user_can_update_own_resume(self):
        resume = self.create_resume(title='Old title')
        self.client.login(username='tester', password='StrongPass123')

        response = self.client.post(
            reverse('resume_update', args=[resume.pk]),
            self.build_resume_payload(title='Updated title'),
        )

        resume.refresh_from_db()
        self.assertRedirects(response, reverse('resume_detail', args=[resume.pk]))
        self.assertEqual(resume.title, 'Updated title')

    def test_user_cannot_view_or_edit_another_users_resume(self):
        resume = self.create_resume(user=self.other_user, title='Private Resume')
        self.client.login(username='tester', password='StrongPass123')

        detail_response = self.client.get(reverse('resume_detail', args=[resume.pk]))
        update_response = self.client.post(
            reverse('resume_update', args=[resume.pk]),
            self.build_resume_payload(title='Hacked title'),
        )

        resume.refresh_from_db()
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(resume.title, 'Private Resume')

    def test_user_can_delete_own_resume(self):
        resume = self.create_resume()
        self.client.login(username='tester', password='StrongPass123')

        response = self.client.post(reverse('resume_delete', args=[resume.pk]))

        self.assertRedirects(response, reverse('resume_list'))
        self.assertFalse(Resume.objects.filter(pk=resume.pk).exists())
