

---

# 🌟 4Stars Project

### 🌟 4Stars Project Overview
4Stars es una plataforma desarrollada para los estudiantes de la Universidad EAFIT, cuyo propósito principal es permitir que los estudiantes evalúen y califiquen a sus profesores. A través de un sistema de calificaciones y reseñas, 4Stars proporciona información valiosa sobre los profesores, ayudando a los estudiantes a tomar decisiones informadas al momento de seleccionar cursos. Este enfoque mejora la experiencia académica al ofrecer una visión clara de los estilos de enseñanza y desempeño de los profesores, promoviendo una experiencia educativa más satisfactoria.

Además, 4Stars sirve como una herramienta de retroalimentación para la universidad, permitiendo a la administración evaluar el rendimiento del profesorado en base a los comentarios de los estudiantes. Al brindar un espacio accesible y transparente, la plataforma busca resolver el problema de la falta de información sobre los profesores antes de la inscripción a las clases, garantizando que la elección de los estudiantes no quede al azar.

---

## 📑 Table of Contents
- [🌟 4Stars Project](#-4stars-project)
    - [🌟 4Stars Project Overview](#-4stars-project-overview)
  - [📑 Table of Contents](#-table-of-contents)
  - [📝 Project Overview](#-project-overview)
  - [🛠 Prerequisites](#-prerequisites)
  - [🏗️ Setup Instructions](#️-setup-instructions)
    - [1. Cloning the Repository](#1-cloning-the-repository)
    - [2. Environment Configuration](#2-environment-configuration)
    - [3. Database Setup](#3-database-setup)
  - [📦 Installation of Requirements](#-installation-of-requirements)
  - [🚀 Running the Project](#-running-the-project)
    - [4. Django and Tailwind Setup](#4-django-and-tailwind-setup)
    - [5. Starting the Services in Parallel](#5-starting-the-services-in-parallel)
      - [6. OS Specific Commands](#6-os-specific-commands)
        - [For Linux/macOS](#for-linuxmacos)
        - [For Windows](#for-windows)
  - [🤝 Contributing](#-contributing)
  - [📧 Contact Us](#-contact-us)
  - [👥 Contributors](#-contributors)

---

## 📝 Project Overview
The **4Stars Project** is built using **Django** as the backend and **Tailwind CSS** for frontend styling. This combination allows for rapid development while maintaining a modern and responsive UI. The platform leverages PostgreSQL as its database, ensuring robustness and scalability.

---

## 🛠 Prerequisites
Before setting up the project, make sure you have the following installed:

- **Python** (3.8 or higher)
- **PostgreSQL**
- **Node.js** (for Tailwind CSS)
- **npm** or **yarn**
- **Django Tailwind** extension

---

## 🏗️ Setup Instructions

### 1. Cloning the Repository
```bash
git clone https://github.com/username/4stars.git
cd 4stars
```

### 2. Environment Configuration
Create a `.env` file in the root of the project with the following credentials to connect to the PostgreSQL database:

```bash
PGHOST='ep-steep-star-a5i8zayx.us-east-2.aws.neon.tech'
PGDATABASE='4stars-db'
PGUSER='4stars-db_owner'
PGPASSWORD='hvS8JjOF1gTq'
```

### 3. Database Setup
Run the following commands to set up the PostgreSQL database:

```bash
python manage.py migrate
```

---

## 📦 Installation of Requirements

Before running the project, you need to install all dependencies for both **Django** and **Tailwind CSS**.

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tailwind and Node.js dependencies**:
   ```bash
   npm install
   ```

---

## 🚀 Running the Project

### 4. Django and Tailwind Setup
To ensure that the project runs smoothly, you’ll need to install the necessary dependencies for both Django and Tailwind.

1. **Install Tailwind**:
    ```bash
    python manage.py tailwind install
    ```

2. **Start Tailwind** in parallel with Django:
    ```bash
    python manage.py tailwind start
    ```

3. **Start Django server**:
    ```bash
    python manage.py runserver
    ```

### 5. Starting the Services in Parallel

For convenience, you can run both the **Django** and **Tailwind** services simultaneously by opening two terminal windows or tabs:

- In the first terminal, run:
    ```bash
    python manage.py runserver
    ```

- In the second terminal, start the Tailwind service:
    ```bash
    python manage.py tailwind start
    ```

Alternatively, you can use the `&` operator to run them in parallel in one terminal (Linux and macOS):
```bash
python manage.py runserver & python manage.py tailwind start
```

#### 6. OS Specific Commands
##### For Linux/macOS
- Clone the repository:
    ```bash
    git clone https://github.com/username/4stars.git
    cd 4stars
    ```
- Install requirements:
    ```bash
    pip install -r requirements.txt
    npm install
    ```
- Run Django and Tailwind in parallel:
    ```bash
    python manage.py runserver & python manage.py tailwind start
    ```

##### For Windows
- Clone the repository:
    ```bash
    git clone https://github.com/username/4stars.git
    cd 4stars
    ```
- Install requirements:
    ```bash
    pip install -r requirements.txt
    npm install
    ```
- Start Django and Tailwind in separate Command Prompt windows:
    - In window 1:
      ```bash
      python manage.py runserver
      ```
    - In window 2:
      ```bash
      python manage.py tailwind start
      ```

---

## 🤝 Contributing
We welcome contributions from the community! Please follow these steps to get involved:

1. Fork the repository.
2. Create a new feature branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature"
    ```
4. Push the branch:
    ```bash
    git push origin feature-branch
    ```
5. Open a Pull Request.

---

## 📧 Contact Us
For any questions or support, feel free to reach out via email:

**Maximiliano Bustamante** – [mbustamang@eafit.edu.co](mailto:mbustamang@eafit.edu.co) 🦝

---

## 👥 Contributors

- **Maximiliano Bustamante**  
- **Valeria Hornung**
- **Nathaly Ramirez**
- **Esteban Duarte**

We appreciate your collaboration and hope you enjoy working with us!

---

