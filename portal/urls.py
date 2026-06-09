from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_detail_view, name='profile_detail'),
    path('skill/add/', views.add_skill, name='add_skill'),
    path('skill/<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('skill/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    path('explore/', views.explore_skills, name='explore'),
    path('request/<int:skill_id>/', views.request_session, name='request_session'),
    path('request/<int:request_id>/respond/<str:action>/', views.respond_request, name='respond_request'),
    path('request/<int:request_id>/complete/', views.complete_request, name='complete_request'),
]
