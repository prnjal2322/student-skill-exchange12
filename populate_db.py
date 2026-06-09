import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_exchange.settings')
django.setup()

from django.contrib.auth.models import User
from portal.models import Profile, Skill, SkillRequest

def populate():
    print("Clearing existing data...")
    SkillRequest.objects.all().delete()
    Skill.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    print("Creating sample users and profiles...")
    
    # 1. Jane
    jane = User.objects.create_user(
        username='jane_doe',
        email='jane@college.edu',
        password='password123',
        first_name='Jane',
        last_name='Doe'
    )
    jane_profile = jane.profile
    jane_profile.department = 'Computer Science'
    jane_profile.bio = 'Junior CS major. Passionate about web development, open source, and artificial intelligence. Always down to help with Python, backend development, or command line queries!'
    jane_profile.contact_info = 'Discord: janedoe#1234 | Email: jane.doe@college.edu'
    jane_profile.save()

    # 2. John
    john = User.objects.create_user(
        username='john_smith',
        email='john@college.edu',
        password='password123',
        first_name='John',
        last_name='Smith'
    )
    john_profile = john.profile
    john_profile.department = 'Creative Design'
    john_profile.bio = 'Digital designer and UI enthusiast. Love prototyping in Figma, editing in Photoshop, and creating layouts. Looking to learn coding and guitar!'
    john_profile.contact_info = 'Email: j.smith@college.edu | Phone: +1-555-0199'
    john_profile.save()

    # 3. Emily
    emily = User.objects.create_user(
        username='emily_w',
        email='emily@college.edu',
        password='password123',
        first_name='Emily',
        last_name='Williams'
    )
    emily_profile = emily.profile
    emily_profile.department = 'Performing Arts'
    emily_profile.bio = 'Music student. Specializing in classical guitar and vocal coaching. I want to learn web development to build a personal portfolio website.'
    emily_profile.contact_info = 'Discord: emily_guitar | Email: ewilliams@college.edu'
    emily_profile.save()

    # 4. David
    david = User.objects.create_user(
        username='david_l',
        email='david@college.edu',
        password='password123',
        first_name='David',
        last_name='Lee'
    )
    david_profile = david.profile
    david_profile.department = 'Foreign Languages'
    david_profile.bio = 'Spanish major. Native speaker from Madrid. Happy to engage in conversational practice. Eager to pick up digital illustration and basic programming!'
    david_profile.contact_info = 'Room 402, Academic Hall | Email: d.lee@college.edu'
    david_profile.save()

    print("Creating sample skills...")
    
    # Jane's skills
    s_python = Skill.objects.create(
        user=jane,
        title='Python Coding',
        description='Can help with basic syntax, loops, data structures, and script writing in Python.',
        category='Programming',
        skill_type='TEACH',
        proficiency='Intermediate'
    )
    s_django = Skill.objects.create(
        user=jane,
        title='Django Backend Web Framework',
        description='Learn how to build REST APIs, database models, templates, and basic routing using Django.',
        category='Programming',
        skill_type='TEACH',
        proficiency='Beginner'
    )
    s_ui_design = Skill.objects.create(
        user=jane,
        title='UI/UX Design Fundamentals',
        description='I need someone to teach me color theory, layout design, typography, and how to create clean interfaces.',
        category='Design',
        skill_type='LEARN',
        proficiency='Beginner'
    )

    # John's skills
    s_figma = Skill.objects.create(
        user=john,
        title='Figma Prototyping',
        description='Interactive components, auto-layouts, wireframing, and user flow designs in Figma.',
        category='Design',
        skill_type='TEACH',
        proficiency='Expert'
    )
    s_photoshop = Skill.objects.create(
        user=john,
        title='Adobe Photoshop Editing',
        description='Photo editing, background removal, layer manipulation, and digital artwork editing.',
        category='Design',
        skill_type='TEACH',
        proficiency='Intermediate'
    )
    s_guitar_learn = Skill.objects.create(
        user=john,
        title='Acoustic Guitar Basics',
        description='I want to learn simple chord progressions, tuning, and basic strumming patterns for popular songs.',
        category='Music',
        skill_type='LEARN',
        proficiency='Beginner'
    )

    # Emily's skills
    s_guitar_teach = Skill.objects.create(
        user=emily,
        title='Classical Guitar Lessons',
        description='Teaching fingerstyle techniques, reading sheet music, chord progressions, and classical composition playing.',
        category='Music',
        skill_type='TEACH',
        proficiency='Expert'
    )
    s_web_learn = Skill.objects.create(
        user=emily,
        title='HTML/CSS & Web Basics',
        description='Need helper guidance to learn HTML tags, flexbox/grid layout styling, and hosting static sites.',
        category='Programming',
        skill_type='LEARN',
        proficiency='Beginner'
    )

    # David's skills
    s_spanish = Skill.objects.create(
        user=david,
        title='Conversational Spanish',
        description='Practice Spanish dialogue, pronunciation, accent reduction, and colloquial terminology.',
        category='Languages',
        skill_type='TEACH',
        proficiency='Expert'
    )

    print("Creating sample skill requests...")
    
    # 1. Request from Jane to John for Figma Prototyping (Status: PENDING)
    SkillRequest.objects.create(
        sender=jane,
        receiver=john,
        skill=s_figma,
        message='Hi John! I saw your post. I can teach you Python in exchange for showing me how to use auto-layouts in Figma. Let me know!',
        status='PENDING'
    )

    # 2. Request from John to Emily for Guitar Lessons (Status: ACCEPTED)
    SkillRequest.objects.create(
        sender=john,
        receiver=emily,
        skill=s_guitar_teach,
        message='Hey Emily, I am looking for beginner guitar lessons. I can help you design layouts for your portfolio website in Figma as an exchange.',
        status='ACCEPTED'
    )

    # 3. Request from David to John for Photoshop (Status: COMPLETED)
    SkillRequest.objects.create(
        sender=david,
        receiver=john,
        skill=s_photoshop,
        message='Hello, I would love to learn some photoshop skills to edit my sketches. I can offer Spanish conversation practice.',
        status='COMPLETED'
    )

    print("Database seeding completed successfully! Created 4 users, 9 skills, and 3 requests.")

if __name__ == '__main__':
    populate()
