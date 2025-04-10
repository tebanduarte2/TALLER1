

---

# 🌟 4Stars Project

### 🌟 4Stars Project Overview
4Stars is a platform developed for the students of EAFIT University, whose main purpose is to allow students to evaluate and rate their professors. Through a system of ratings and reviews, 4Stars provides valuable information about professors, helping students make informed decisions when selecting courses. This approach enhances the academic experience by offering a clear view of teaching styles and professors' performance, promoting a more satisfying educational experience.

Additionally, 4Stars serves as a feedback tool for the university, allowing the administration to assess professors' performance based on student feedback. By providing an accessible and transparent space, the platform seeks to solve the issue of insufficient information about professors before course enrollment, ensuring that students' choices are not left to chance.

---

## 📑 Table of Contents
- [🌟 4Stars Project](#-4stars-project)
    - [🌟 4Stars Project Overview](#-4stars-project-overview)
  - [📑 Table of Contents](#-table-of-contents)
  - [📝 Project Overview](#-project-overview)
  - [🛠 Prerequisites](#-prerequisites)
  - [🏗️ Setup Instructions](#️-setup-instructions)
    - [1. Cloning the Repository](#1-cloning-the-repository)
    - [2. Database Setup](#3-database-setup)
  - [📦 Installation of Requirements](#-installation-of-requirements)
  - [🚀 Running the Project](#-running-the-project)
    - [3. Django and Tailwind Setup](#4-django-and-tailwind-setup)
    - [4. Starting the Services in Parallel](#5-starting-the-services-in-parallel)
      - [5. OS Specific Commands](#6-os-specific-commands)
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


### 2. Database Setup
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

### 3. Django and Tailwind Setup
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

### 4. Starting the Services in Parallel

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

#### 5. OS Specific Commands
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


## 👥 Contributors

- **Maximiliano Bustamante**  
- **Valeria Hornung**
- **Nathaly Ramirez**
- **Esteban Duarte**
- **Gia Mariana Calle**

We appreciate your collaboration and hope you enjoy working with us!

---

