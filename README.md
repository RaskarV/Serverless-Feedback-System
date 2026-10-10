@'
# Serverless Feedback Management System

A serverless web application that enables students to submit feedback on academic sessions and allows faculty to manage sessions and analyze feedback.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Backend:** Python, AWS Lambda
- **API:** Amazon API Gateway
- **Database:** Amazon DynamoDB
- **Hosting:** Amazon S3

## Features

- **Role-Based Login:** Separate access flows for students and faculty.
- **Session Management:** Faculty can create feedback sessions.
- **Feedback Submission:** Students can submit feedback for available sessions.
- **Analytics Dashboard:** Faculty can view feedback statistics and session-wise visualizations.
- **REST API Integration:** Connects the frontend to serverless backend functions and DynamoDB.

## Architecture

1. The frontend is hosted on Amazon S3.
2. API Gateway exposes endpoints for application operations.
3. AWS Lambda processes incoming requests using Python.
4. DynamoDB stores user, session, and feedback records.
5. Chart.js visualizes feedback analytics on the faculty dashboard.

## Project Structure

```text
Serverless-Feedback-System/
├── Frontend/
│   └── index.html
├── backend/
│   └── lambda_fun.py
├── .gitignore
└── README.md
