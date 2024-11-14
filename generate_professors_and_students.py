import os
import time  # To introduce pauses between requests
import json
from dotenv import load_dotenv
import google.generativeai as genai
import django

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fourStarsProject.settings")  # Ensure this points to your Django project settings
django.setup()

from fourStars.models import Professor, Student  # Import your models (adjust the import to match your app name)

# Load API Key from .env
_ = load_dotenv('api_keys.env')
genai.configure(api_key=os.getenv('gemini_api_key'))

# Gemini generative model
model = genai.GenerativeModel('gemini-pro')

# Instruction to generate a neutral professor description
instruction_professor = """
Genera un nombre completo para un profesor universitario, con un correo electrónico asociado. El correo debe ser en el formato profesor@universidad.edu.co,donde dice profesor se debre reemplazar el nombre del profesor para completar el email, solamente debes escribir el nombre y el mail separados por comas, es lo unico que escribiras como respuesta, ejemplo de respuesta
nombre,apellido,email. todo siempre separado por comas, no debes incluir ningun otro texto que no sea ese
"""

instruction_student = """
Genera un nombre completo para un estudiante universitario, con un correo electrónico asociado. El correo debe ser en el formato estudiante@universidad.edu.co en donde dice estudiante se debre reemplazar el nombre del estudiante para completar el email solamente debes escribir el nombre y el mail separados por comas, es lo unico que escribiras como respuesta, ejemplo de respuesta
nombre,apellido,email. todo siempre separado por comas, no debes incluir ningun otro texto que no sea ese
"""

# Helper function to generate content with safety check
def generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        # Check for candidates and safety ratings
        if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            print(f"Safety ratings: {response.candidates[0].safety_ratings}")
        # If no issues, return the text
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"Error generating content: {e}")
    return "No disponible"

# Function to create and save professors
def create_professors(num_professors=25):
    for i in range(num_professors):
        print(f"Creating professor {i+1}")

        # Generate professor name and email
        prompt_professor = f"{instruction_professor} Haz una generación para un profesor universitario."
        professor_info = generate_content(prompt_professor)
        
        print(f"Gemini response for professor {i+1}: {professor_info}")  # Debug: Print the output from Gemini

        if professor_info and "@" in professor_info:
            try:
                # Split by space and at sign to capture name and email
                first_name, last_name, email = professor_info.split(",")

                # Save professor to the database
                professor = Professor(first_name=first_name, last_name=last_name, email=email)
                professor.save()
                print(f"Created Professor: {first_name} {last_name} - {email}")
            except ValueError as e:
                print(f"Error unpacking the response for professor {i+1}: {e}")
                continue  # Skip this entry if there's a formatting issue
        else:
            print(f"Invalid format for professor {i+1}: {professor_info}")

        # Pause to respect API limits
        time.sleep(3)

# Function to create and save students
def create_students(num_students=25):
    for i in range(num_students):
        print(f"Creating student {i+1}")

        # Generate student name and email
        prompt_student = f"{instruction_student} Haz una generación para un estudiante universitario."
        student_info = generate_content(prompt_student)
        
        print(f"Gemini response for student {i+1}: {student_info}")  # Debug: Print the output from Gemini

        if student_info and "@" in student_info:
            try:
                # Split by space and at sign to capture name and email
                first_name, last_name, email = student_info.split(",")

                # Save student to the database
                password = 'password123'  # You can randomize this if needed
                student = Student(first_name=first_name, last_name=last_name, email=email, password=password)
                student.save()
                print(f"Created Student: {first_name} {last_name} - {email}")
            except ValueError as e:
                print(f"Error unpacking the response for student {i+1}: {e}")
                continue  # Skip this entry if there's a formatting issue
        else:
            print(f"Invalid format for student {i+1}: {student_info}")

        # Pause to respect API limits
        time.sleep(3)

if __name__ == "__main__":
    create_professors()  # Create
    create_students()  # Create 25 students
