from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Profile, Skill, SkillRequest
from .forms import RegistrationForm, ProfileForm, SkillForm, SkillRequestForm


def landing(request):
    """
    Renders the public landing page with platform stats and a few featured skills.
    """
    recent_skills = Skill.objects.all().order_by('-created_at')[:6]
    
    # Platform stats
    total_users = User.objects.count()
    total_skills = Skill.objects.count()
    total_requests = SkillRequest.objects.count()
    completed_exchanges = SkillRequest.objects.filter(status='COMPLETED').count()

    context = {
        'recent_skills': recent_skills,
        'total_users': total_users,
        'total_skills': total_skills,
        'total_requests': total_requests,
        'completed_exchanges': completed_exchanges,
    }
    return render(request, 'portal/landing.html', context)


def register_view(request):
    """
    Registers a new student, automatically logs them in, and redirects to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to Skill Exchange, {user.first_name}! Your profile has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegistrationForm()
    
    return render(request, 'portal/register.html', {'form': form})


def login_view(request):
    """
    Authenticates an existing student.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    """
    Logs out the user.
    """
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('landing')


@login_required
def dashboard(request):
    """
    Displays user profile details, posted skills, and incoming/outgoing session requests.
    """
    # Fetch user's skills
    my_skills = Skill.objects.filter(user=request.user).order_by('-created_at')
    
    # Fetch requests received (incoming)
    received_requests = SkillRequest.objects.filter(receiver=request.user).order_by('-created_at')
    
    # Fetch requests sent (outgoing)
    sent_requests = SkillRequest.objects.filter(sender=request.user).order_by('-created_at')

    # Stats calculation
    teaching_count = my_skills.filter(skill_type='TEACH').count()
    learning_count = my_skills.filter(skill_type='LEARN').count()
    pending_incoming = received_requests.filter(status='PENDING').count()
    completed_sessions = (
        received_requests.filter(status='COMPLETED').count() + 
        sent_requests.filter(status='COMPLETED').count()
    )

    context = {
        'profile': request.user.profile,
        'my_skills': my_skills,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
        'teaching_count': teaching_count,
        'learning_count': learning_count,
        'pending_incoming': pending_incoming,
        'completed_sessions': completed_sessions,
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def edit_profile_view(request):
    """
    Edits user bio, department, and contact info.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'portal/profile_form.html', {'form': form})


def profile_detail_view(request, username):
    """
    Renders public or peer-viewable profile card of a specific user.
    """
    profile_user = get_object_or_404(User, username=username)
    user_skills = Skill.objects.filter(user=profile_user).order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'profile': profile_user.profile,
        'skills': user_skills,
    }
    return render(request, 'portal/profile.html', context)


@login_required
def add_skill(request):
    """
    Adds a new skill to teach or learn.
    """
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, f"Skill '{skill.title}' posted successfully!")
            return redirect('dashboard')
    else:
        form = SkillForm()
    
    return render(request, 'portal/skill_form.html', {'form': form, 'title': 'Post a New Skill'})


@login_required
def edit_skill(request, skill_id):
    """
    Modifies an existing skill.
    """
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user != request.user:
        messages.error(request, "You do not have permission to edit this skill.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f"Skill '{skill.title}' updated successfully.")
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'portal/skill_form.html', {'form': form, 'title': f"Edit Skill: {skill.title}", 'edit_mode': True})


@login_required
def delete_skill(request, skill_id):
    """
    Deletes a skill from user profile.
    """
    skill = get_object_or_404(Skill, id=skill_id)
    if skill.user != request.user:
        messages.error(request, "You do not have permission to delete this skill.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully.")
        return redirect('dashboard')
    
    return render(request, 'portal/skill_confirm_delete.html', {'skill': skill})


def explore_skills(request):
    """
    Lists skills posted by other users. Provides search functionality by title,
    description, username, and filter by category or type (TEACH/LEARN).
    """
    skills_list = Skill.objects.exclude(user=request.user) if request.user.is_authenticated else Skill.objects.all()
    
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    skill_type = request.GET.get('type', '')
    
    if query:
        skills_list = skills_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query)
        )
    
    if category:
        skills_list = skills_list.filter(category=category)
        
    if skill_type:
        skills_list = skills_list.filter(skill_type=skill_type)

    skills_list = skills_list.order_by('-created_at')

    # Import categories list for sidebar options
    from .models import CATEGORY_CHOICES

    context = {
        'skills': skills_list,
        'query': query,
        'selected_category': category,
        'selected_type': skill_type,
        'categories': CATEGORY_CHOICES,
    }
    return render(request, 'portal/explore.html', context)


@login_required
def request_session(request, skill_id):
    """
    Form view to request a session with the skill owner.
    """
    skill = get_object_or_404(Skill, id=skill_id)
    
    if skill.user == request.user:
        messages.error(request, "You cannot request your own skill.")
        return redirect('explore')
        
    # Check if request already exists
    existing_request = SkillRequest.objects.filter(sender=request.user, receiver=skill.user, skill=skill).exclude(status__in=['DECLINED', 'COMPLETED']).first()
    if existing_request:
        messages.info(request, f"You already have a active '{existing_request.status}' request for this skill.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            skill_request = form.save(commit=False)
            skill_request.sender = request.user
            skill_request.receiver = skill.user
            skill_request.skill = skill
            skill_request.status = 'PENDING'
            skill_request.save()
            messages.success(request, f"Request sent successfully to {skill.user.first_name or skill.user.username}!")
            return redirect('dashboard')
    else:
        form = SkillRequestForm()
        
    context = {
        'form': form,
        'skill': skill,
    }
    return render(request, 'portal/request_form.html', context)


@login_required
def respond_request(request, request_id, action):
    """
    Accepts or declines an incoming skill session request.
    """
    skill_request = get_object_or_404(SkillRequest, id=request_id)
    
    if skill_request.receiver != request.user:
        messages.error(request, "You do not have permission to respond to this request.")
        return redirect('dashboard')
        
    if action == 'accept':
        skill_request.status = 'ACCEPTED'
        messages.success(request, f"You accepted the request from {skill_request.sender.first_name}!")
    elif action == 'decline':
        skill_request.status = 'DECLINED'
        messages.info(request, f"You declined the request from {skill_request.sender.first_name}.")
    else:
        messages.error(request, "Invalid action.")
        
    skill_request.save()
    return redirect('dashboard')


@login_required
def complete_request(request, request_id):
    """
    Marks a session request as completed (can be done by either sender or receiver).
    """
    skill_request = get_object_or_404(SkillRequest, id=request_id)
    
    if request.user != skill_request.sender and request.user != skill_request.receiver:
        messages.error(request, "You are not authorized to manage this request.")
        return redirect('dashboard')
        
    if skill_request.status != 'ACCEPTED':
        messages.error(request, "Only accepted sessions can be marked as completed.")
        return redirect('dashboard')
        
    skill_request.status = 'COMPLETED'
    skill_request.save()
    messages.success(request, "Session marked as completed. Keep up the learning!")
    return redirect('dashboard')
