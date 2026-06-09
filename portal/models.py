from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Choices definitions
CATEGORY_CHOICES = [
    ('Programming', 'Programming & Tech'),
    ('Design', 'Design & Creative'),
    ('Music', 'Music & Arts'),
    ('Languages', 'Languages'),
    ('Academics', 'Academics & Tutoring'),
    ('Fitness', 'Fitness & Sports'),
    ('Others', 'Others'),
]

TYPE_CHOICES = [
    ('TEACH', 'Teach (I can teach this skill)'),
    ('LEARN', 'Learn (I want to learn this skill)'),
]

PROFICIENCY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Expert', 'Expert'),
]

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('ACCEPTED', 'Accepted'),
    ('DECLINED', 'Declined'),
    ('COMPLETED', 'Completed'),
]


class Profile(models.Model):
    """
    Extends the default Django User model to store student-specific details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500, help_text="Tell others about yourself, your interests, etc.")
    department = models.CharField(max_length=100, blank=True, help_text="e.g. Computer Science, Mechanical Engineering")
    contact_info = models.CharField(max_length=150, blank=True, help_text="e.g. email@example.com, phone number, Discord tag")

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Skill(models.Model):
    """
    Represents a skill a user either wants to teach or learn.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=100, help_text="e.g. Python, Photoshop, Guitar, Spanish")
    description = models.TextField(help_text="Provide details about what you want to teach or learn.")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Programming')
    skill_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='TEACH')
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Intermediate')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        skill_type_label = "Teaching" if self.skill_type == "TEACH" else "Learning"
        return f"{self.user.username} - {skill_type_label} {self.title} ({self.proficiency})"


class SkillRequest(models.Model):
    """
    Tracks session or exchange requests between students.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requests')
    message = models.TextField(blank=True, help_text="Introduce yourself and propose a schedule or exchange details.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} for '{self.skill.title}' ({self.status})"


# Signals to automatically create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists before saving (handles cases where users were created without a profile)
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
