# BloomFiltering

This project demonstrates the usage of Bloom filtering to eliminate the usage of leaked/weak or slightly modified passwords from users. It takes advantage of the Django Rest Framework to accomplish its objectives. 

The project is divided into two main objectives:

1. **Checking Password Strength**:
   This objective uses the Bloom filtering technique to allow users to register or change their passwords. It is accomplished by:
   1. Training the program on datasets to create the Bloom filter bit array.
   2. During the training process, the program splits the password into bigrams. Each bigram is hashed using 15 hashing algorithms, and a bitwise OR operation is performed to get the final index to be marked in the bit array.

2. **Using the Jaccard Coefficient**:
   This objective finds the similarity between two given passwords. It is accomplished by:
   1. Creating two temporary Bloom filtering arrays.
   2. Training each array on one of the passwords given by the user to check the similarity.
   3. The training process involves splitting the password into bigrams and using 15 hashing algorithms on each bigram, which will get the final index to mark using the bitwise OR operation.
   4. Using the Jaccard Coefficient algorithm on the two temporarily generated Bloom filters to find the similarity.
      
# Django Usage

To accomplish the goal of this project, the Django Rest Framework was used, and two apps were created for this project:

1. **bloomfilter**:
   This app is responsible for:
   1. Creating the Bloom filter object.
   2. Creating the methods/functions to determine the strength of passwords.
   3. Implementing the Jaccard Coefficient in the bloomfilter app.
  
2. **customUser**:
   This app is responsible for:
   1. Creating the user object.
   2. Creating the functions that the user needs to perform actions such as registering, logging in, changing passwords, etc.
   3. The functions also call the methods/functions from the bloomfilter app to check the strength of the password before taking actions that involve checking the password strength.
   
The customUser application takes advantage of the Django authentication method.
   
 
## Steps to Run the `password_similarity_project`

### Step 1: Create a New Environment

- Create a new environment (outside the `password_similarity_project` folder):  
  - Linux: `python3 -m venv myenv`  
  - Windows: `python -m venv myenv`
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
