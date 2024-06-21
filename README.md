# BloomFiltering

## Steps to Run the password_similarity_project

### Step 1: Create a New Environment

- Create a new environment (outside the password_similarity_project folder):  
  `python -m venv myenv`
- Activate the environment:  
  - Linux: `source myenv/bin/activate`  
  - Windows: `myenv\Scripts\activate`

### Step 2: Install Dependencies

- Navigate to the directory: `cd password_similarity_project`
- Install required packages:  
  `pip install -r requirements.txt`

### Step 3: Database Migrations and Server Start

- Prepare database migrations:  
  `python manage.py makemigrations`
- Apply migrations:  
  `python manage.py migrate`
- Start the server:  
  `python manage.py runserver`
