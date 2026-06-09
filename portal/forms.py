from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, SkillRequest

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Input a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'department', 'contact_info']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell others about your skills, background, and availability...'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science, Graphic Design, Business'}),
            'contact_info': forms.TextInput(attrs={'placeholder': 'e.g. email@college.edu, Discord: username, or phone number'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category', 'skill_type', 'proficiency']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Python Programming, Classical Guitar, Figma UX/UI'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe what you can teach or what you want to learn in detail...'}),
            'category': forms.Select(),
            'skill_type': forms.Select(),
            'proficiency': forms.Select(),
        }


class SkillRequestForm(forms.ModelForm):
    class Meta:
        model = SkillRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Introduce yourself, specify when you are free, or ask questions...'}),
        }
