Requirements:
Python 3.11+

pip (Python package manager)

virtualenv 

Git 
Step 1:
Clone the git hub repository
cd Hello
Step 2: 
Create an Active virtual environment
python -m venv venv
venv\Scripts\activate
Step 3:
Install the depedencies
pip install -r requirements.txt
Step 4:
Apply database migrations
python manage.py migrate
Step 5:
Create a superuser
python manage.py createsuperuser
Step 6:
Run the development server
python manage.py runserver
Step 7 :
Access the appliaction on http://127.0.0.1:8000/admin