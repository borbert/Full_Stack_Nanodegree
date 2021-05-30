# Full Stack Nanodegree Progam -- Udacity

This repository is for the projects completed during the [Full Stack Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) at [Udacity](https://www.udacity.com/). This README serves as an overveiw and a table of contents for the projects completed.

## Projects

1. [Fyyur](https://github.com/borbert/Full_Stack_Nanodegree/tree/master/01_fyyur#fyyur)

   Aim of the project was to build a full-stack Web App with Flask and Boostrap which enables
   Venues & Artists to list themselves and arrange Shows together.

   Used tech stack:

   - `SQLAlchemy` as ORM library of choice
   - `PostgreSQL` as database
   - `Python3` and `Flask` for server language and framework
   - `Flask-Migrate` for creating and running schema migrations
   - Frontend: HTML, CSS, and Javascript with Bootstrap 3 (mainly provided by Udacity Team)

   Applied concepts:

   - How to use Git Bash & Github as version control tool
   - Configure local database and connect it to a web application
   - Create Model Schemas with columns and relationships (1:1, 1:n and N:N)
   - Use SQLAlchemy ORM with PostgreSQL to query, insert, edit & delete Data
   - Use WTForms to encapsulate input forms in seperate file & to allow for custom validations
   - Use Boostrap as a simple to use Front End Libary and Ajax to fetch flask routes
   - Create SQL-like Queries, but without any SQL syntax, only using SQLAlchemy ORM
   - How to clearly structurize a larger web application in different files & folders

   [View running website]()

2. [Full Stack Trivia App](https://github.com/borbert/Full_Stack_Nanodegree/tree/master/02_trivia_ap#full-stack-api-final-project)

   Using 'Flask' and 'React', created a Full-Stack App to manage questions
   for different categories & develop an API to power the Quiz Gameplay.

   Used tech stack:

   - React Components as frontend (provided by Udacity Team)
   - Python3 and Flask for server language and API development
   - `cors` to handle access to the API
   - `unittest` for automated testing of APIs
   - `curl` to get responses from API
   - `README.md` to document project setup & API endpoints

   Applied concepts:

   - using best-practice `PEP8-style` to design and structur code
   - `test-driven-development (TDD)` to rapidly create highly tested & maintainable endpoints.
   - directly test and make response to any endpoint out there with `curl`.
   - implement `errorhandler` to format & design appropiate error messages to client
   - becoming aware of the importance of extensive project documentation & testing.

   [View running website]()

3. [Coffee Shop App](https://github.com/borbert/Full_Stack_Nanodegree/tree/master/03_coffee_shop_full_stack#coffee-shop-full-stack)

   Using 'Flask' and 'Auth0', created a Full-Stack App to let Users
   login to Site & make actions according to their Role & Permission Sets.

   Used tech stack:

   - `Python3` & `Flask` for server language and API development
   - `SQLAlchemy` as ORM / `Sqlite` as database
   - `Ionic` to serve and build the frontend (provided by Udacity Team)
   - `Auth0` as external Authorization Service & permission creation
   - `jose` JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTs.
   - `postman` to automatize endpoint testing & verification of correct Authorization behaviour.

   [View running website]()

4. [Deployment to Kudernetes](https://github.com/borbert/Full_Stack_Nanodegree/tree/master/Deploy%20to%20Kubernetes%20Using%20EKS#deploying-a-flask-api)

   Deployed a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

   (Application has been teared down after successfull review to avoid incurring additional costs)

   Used tech stack:

   - `Docker` for app containerization & image creation to ensure environment consistency across development and production server
   - `AWS EKS` & `Kubernetes` as container orchestration service to allow for horizontal scaling
   - `aswscli` to interact with AWS Cloud Services
   - `ekscli` for EKS cluster creation
   - `kubectl` to interact with kubernetes cluster & pods
   - `CodePipeline` for Continuous Delivery (CD) & to watch Github Repo for changes
   - `CodeBuild` for Continuous Integration (CI), together with `pytest` for automated testing before deployment

# [Capstone Project](https://github.com/borbert/Full_Stack_Nanodegree/tree/master/capstone#intro)

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku` (see `setup.sh`)

[View website]()
