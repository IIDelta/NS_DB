@echo off

REM Activate the virtual environment
call venv\Scripts\activate

REM Run the Django development server
python manage.py runserver

REM Keep the command prompt open (optional)
cmd
