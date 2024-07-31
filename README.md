
Project Overview
This project is based on an open-source Django application. It includes the addition of a user authentication system and a Document Query System that allows users to upload PDFs and query them. The application has been containerized using Docker and deployed to AWS Lambda.

Project Details
Chosen Project
I have created this project from scratch 

Added Functionality
User Authentication System:
RAG application

Allows users to sign in using a username and password.
Document Query System:

Users can upload PDFs and input queries.
The system processes the PDF and returns answers based on the query.
Dockerization
The application has been containerized using Docker. The Dockerfile ensures that the application, along with all necessary dependencies, is packaged into a Docker image.

Dockerfile
The Dockerfile includes:

Installation of necessary build dependencies.
Installation of Python dependencies specified in requirements.txt.
Setup of the working directory.
Configuration for running the Django application using Uvicorn.


AWS Lambda Deployment
The Dockerized application has been deployed to AWS Lambda using AWS API Gateway to expose the application’s endpoints.

Steps to Deploy
Create an ECR Repository:

aws ecr create-repository --repository-name my-lambda-repo --region <your-region>
Build and Push Docker Image to ECR:

# Authenticate Docker to ECR
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<your-region>.amazonaws.com

# Build Docker image
docker build -t my-lambda-image .

# Tag Docker image
docker tag my-lambda-image:latest <account-id>.dkr.ecr.<your-region>.amazonaws.com/my-lambda-repo:latest

# Push Docker image to ECR
docker push <account-id>.dkr.ecr.<your-region>.amazonaws.com/my-lambda-repo:latest
Create a Lambda Function:

Configure the Lambda function to use the Docker image from ECR.
Configure API Gateway:

Create a new HTTP API.
Set up routes and methods to map to your Lambda function.
Deploy the API to make it accessible.
Testing the Application
Login Endpoint: Use a POST request to https://<api-id>.execute-api.<your-region>.amazonaws.com/login with username and password fields.
Document Query Endpoint: After logging in, use a POST request to https://<api-id>.execute-api.<your-region>.amazonaws.com/index with query and pdf fields (PDF file should be uploaded as multipart/form-data).
Documentation
How to Run Locally:

Clone the repository.
Install Docker.
Build the Docker image using the provided Dockerfile.
Run the Docker container locally.
