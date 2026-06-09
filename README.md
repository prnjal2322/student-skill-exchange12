# Student Skill Exchange

A web-based platform designed for students to connect, share, and exchange academic and practical skills. Whether it is mastering a programming language, learning graphic design, or grasping complex engineering concepts, this platform facilitates peer-to-peer collaborative learning.

## 🚀 Features

* **User Authentication:** Secure registration and login profiles for students.
* **Skill Matchmaking:** Post skills you offer and search for skills you want to learn.
* **Interactive Dashboard:** Manage active skill exchanges and connections.
* **Responsive UI:** Clean, user-friendly interface optimized for both desktop and mobile browsing.

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Frontend:** HTML5, CSS3, Bootstrap

## 📋 Prerequisites

Before running the project locally, ensure you have the following installed:
* Python 3.8 or higher
* pip (Python package installer)
* Git

## 🔧 Installation & Setup

Follow these steps to get your development environment running:

1. **Clone the Repository**
```bash
   git clone [https://github.com/prnjal2322/student-skill-exchange12.git](https://github.com/prnjal2322/student-skill-exchange12.git)
   cd student-skill-exchange12

2.Create a Virtual Environment

Bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

3. Install Dependencies

Bash
   pip install -r requirements.txt
(Note: If you don't have a requirements.txt yet, install Django using pip install django)

4.Apply Database Migrations

Bash
   python manage.py migrate
Create a Superuser (Admin Access)

Bash
   python manage.py createsuperuser
Run the Development Server

Bash
   python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/ to view the application.

📂 Project Structure
Plaintext
student-skill-exchange12/
│
├── manage.py            # Django command-line utility
├── db.sqlite3           # Local development database
├── .gitignore           # Specifies intentionally untracked files to ignore
├── populate_db.py       # Script to populate the database with dummy data
└── student_skill_exchange/  # Main project directory
🤝 Contributing
Contributions are welcome! If you'd like to improve the platform, please fork the repository and create a pull request, or open an issue with your suggestions.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


***

### How to add this to your repository:
1. On your GitHub repository page (shown in `17809862034621158483002912560142_5de564.jpg`), click the big **Add a README** button.
2. Clear any default text and paste the markdown block above into the editor.
3. Scroll down and click **Commit changes...** to save it directly to your main branch.

http://googleusercontent.com/interactive_content_block/0
