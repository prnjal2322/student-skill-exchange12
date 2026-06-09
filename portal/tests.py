from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Skill, SkillRequest

class ModelSignalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@college.edu',
            password='testpassword123',
            first_name='Test',
            last_name='Student'
        )

    def test_profile_auto_created_signal(self):
        """
        Verify that a Profile is automatically created when a User is created.
        """
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.user, self.user)
        self.assertEqual(self.user.profile.bio, '')
        
    def test_profile_save_signal(self):
        """
        Verify that updating the user profile model updates and saves properly.
        """
        profile = self.user.profile
        profile.department = 'Computer Science'
        profile.bio = 'Hello world!'
        profile.save()
        
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.department, 'Computer Science')
        self.assertEqual(updated_profile.bio, 'Hello world!')


class SkillAndRequestTestCase(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(
            username='teacher', password='password123', first_name='Teacher', last_name='A'
        )
        self.user2 = User.objects.create_user(
            username='learner', password='password123', first_name='Learner', last_name='B'
        )
        
        # Create a skill owned by user1
        self.skill = Skill.objects.create(
            user=self.user1,
            title='Python Programming',
            description='I can teach Python fundamentals.',
            category='Programming',
            skill_type='TEACH',
            proficiency='Expert'
        )

    def test_skill_creation(self):
        """
        Verify skill creation details.
        """
        self.assertEqual(self.skill.title, 'Python Programming')
        self.assertEqual(self.skill.user, self.user1)
        self.assertEqual(self.skill.skill_type, 'TEACH')
        self.assertEqual(str(self.skill), 'teacher - Teaching Python Programming (Expert)')

    def test_skill_request_flow(self):
        """
        Test creating a skill request and responding to it.
        """
        # Create request from user2 (learner) to user1 (teacher)
        req = SkillRequest.objects.create(
            sender=self.user2,
            receiver=self.user1,
            skill=self.skill,
            message='I want to learn Python!',
            status='PENDING'
        )
        
        self.assertEqual(req.status, 'PENDING')
        self.assertEqual(req.sender, self.user2)
        self.assertEqual(req.receiver, self.user1)
        
        # Accept request
        req.status = 'ACCEPTED'
        req.save()
        self.assertEqual(req.status, 'ACCEPTED')
        
        # Complete request
        req.status = 'COMPLETED'
        req.save()
        self.assertEqual(req.status, 'COMPLETED')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='alex', password='password123', first_name='Alex', last_name='Smith'
        )
        self.user2 = User.objects.create_user(
            username='bob', password='password123', first_name='Bob', last_name='Jones'
        )
        
        self.skill1 = Skill.objects.create(
            user=self.user1,
            title='Figma Design',
            description='Learn Figma basics',
            category='Design',
            skill_type='TEACH',
            proficiency='Intermediate'
        )
        self.skill2 = Skill.objects.create(
            user=self.user2,
            title='Guitar chords',
            description='Strumming patterns',
            category='Music',
            skill_type='TEACH',
            proficiency='Beginner'
        )

    def test_landing_page_view(self):
        """
        Landing page should respond successfully.
        """
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Figma Design')
        self.assertContains(response, 'Guitar chords')

    def test_explore_search_and_filters(self):
        """
        Explore view should support search query and category parameters.
        """
        # Test basic search query
        response = self.client.get(reverse('explore'), {'q': 'Figma'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Figma Design')
        self.assertNotContains(response, 'Guitar chords')
        
        # Test category filters
        response = self.client.get(reverse('explore'), {'category': 'Music'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Guitar chords')
        self.assertNotContains(response, 'Figma Design')

    def test_dashboard_requires_login(self):
        """
        Accessing the dashboard without logging in should redirect to the login page.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))
