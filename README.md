# Full Stack Blog Project in Python

## About the Project

This project is a Capstone project in the Udemy Course - *100 Days of Code: The Complete Python Pro Bootcamp* by Doctor Angela Yu. It combines all the content learned from Days 54 through to Day 71, which includes HTML and CSS, Flask, Flask Forms, templating, databases, APIs and authentication. I highly recommend the course for anyone who is interested
in learning about coding in Python, regardless of what level they are at.

The project involved 4 stages
- Templating routes (e.g. home, about, contact pages)
- Adding styling using Bootstrap
- Restful Routing
- Adding Users and Authentication

I wasn't super interested in exploring the HTML and CSS aspects of this project as I have already done a similar thing when I implemented a full stack blog using React. However,
I was interested in exploring the Backend elements of this project. In particular, I was interested in learning about the Flask framework and SQLalchemy library in comparison to Node JS. 

While I have largely implemented this project following the instructions laid out in the course, I plan to implement some extensions to the functionality as laid out below.
Additionally, I plan to revisit my react-blog project and re-explore authentication in Node JS. 

## Skills Learned

- Implementing a flask framework
    - HTTP routes
    - Python Decorators
    - Jinja templating
- Forms in Flask
    - Using and rendering Flask wtf forms 
    - Form validators (e.g. data required, minimum length etc.)
- Authentication in Flask
    - Logging in users
    - Securely storing and hasing passwords
    - Protecting routes
    - Writing custom decorators (e.g. checking if a user is an admin)
- Working with SQLalchmey to call a Postgres database
    - CRUD operations
    - Relational databases
- RESTful routing

## Extensions

### Authentication

- Limit the number of password attempts which users can enter on a given account
- Implement a password resetting mechanism
- Implement alternative methods of signing in (e.g. google OAUTH)
- Rate limits

### User Experience

- Allow the user who made the original comment to delete their comments
- Allow the admin user to delete any comment