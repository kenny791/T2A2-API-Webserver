# T2A2 API Webserver
[Github Repo](https://github.com/kenny791/T2A2-API-Webserver)

## Table Of Contents  
[R1 - Identification of the problem you are trying to solve by building this particular app.](#r1-identification-of-the-problem-you-are-trying-to-solve-by-building-this-particular-app)  
[R2 - Why is it a problem that needs solving?](#r2-why-is-it-a-problem-that-needs-solving)  
[R3 Why have you chosen this database system. What are the drawbacks compared to others?](#r3-why-have-you-chosen-this-database-system-what-are-the-drawbacks-compared-to-others)  
[R4 Identify and discuss the key functionalities and benefits of an ORM](#r4-identify-and-discuss-the-key-functionalities-and-benefits-of-an-orm)  
[R5 Document all endpoints for your API](#r5-document-all-endpoints-for-your-api)  
[R6 An ERD for your app](#r6-an-erd-for-your-app)  
[R7 Detail any third party services that your app will use](#r7-detail-any-third-party-services-that-your-app-will-use)  
[R8 Describe your projects models in terms of the relationships they have with each other](#r8-describe-your-projects-models-in-terms-of-the-relationships-they-have-with-each-other)   
[R9 Discuss the database relations to be implemented in your application](#r9-discuss-the-database-relations-to-be-implemented-in-your-application)  
[R10 Describe the way tasks are allocated and tracked in your project](#r10-describe-the-way-tasks-are-allocated-and-tracked-in-your-project)  
[Getting Started](#getting-started)


---
## R1 Identification of the problem you are trying to solve by building this particular app.  
Like many foodies, I enjoy trying out new restaurants and cuisines. However the amount of restaurants you have to choose from can be overwhelming, and when you have tried the restaurant it is hard to keep track of the ones you like.

---
## R2 Why is it a problem that needs solving?  
With the cost of living ever increasing in Australia, it is important to find the best value for money, and making sure every new visit is worthwhile. With this app you can find new restaurants submitted by like minded foodies, seeing their reviews and ratings. Once you have visited a restaurant you can add your own review and rating so others can benefit from the information. This app will also allow you to save restaurants you like to your account, and keep track of the ones you would like to try and the ones you thought were great.

---
## R3 Why have you chosen this database system. What are the drawbacks compared to others?  
The database system chosen for this project is a relational database system specifically PostgreSQL. The data for the app will be stored in a consistent format in each table, this is important as it allows for the data to be more easily accessed and manipulated. For example if a table has a date attribute, all the dates will be stored in the same format according to the schema, making it easier to sort and filter the data.  
Additionally as the data will be stored in tables with unique id keys for each entry this will allow for the tables to be joined and relationships formed allowing for data to be accessed and manipulated at the same time.


### Benefits of using PostgreSQL
- <b>Object-relational database management system</b>: It has all the features of a
relational database, with additional features such as inheritance and function
overloading, which allows for more complicated data structures
- <b>Materialised views</b>: a pre-computed query result that can be recalled later
- <b>Security features</b>: allows for file protection and users authentication
- <b>Supports MVCC</b>: multi-version concurrency control, allowing for different users to
interact with and manage the database simultaneously.
- <b>Supports multiple programming platforms</b>: such as C, C++, Java, Python
- <b>Point-In-Time Recovery</b>: which allows the restoration of the database from a point in
time.

### Drawbacks of using PostgreSQL:
- <b>Speed</b>: the speed and performance is not as high when compared to other relational
databases such as MySQL.
- <b>Usability</b>: the learning curve is considered to be difficult.
- <b> Documentation</b>: support is not as common as others.

---
## R4 Identify and discuss the key functionalities and benefits of an ORM  
Object Relational Mapping (ORM) is a technique using libraries to represent tables in a relational database as objects in object-oriented programming languages. This allows for CRUD operations to be performed on the database using object-oriented programming languages, such as Python and Javascript.

  
### Benefits  
- Allows for creation of dynamic queries. For example a user can search for a restaurant by name, or by cuisine type, or by location. This can be done by creating a dynamic query that will search for the restaurant based on the parameters provided by the user. 
- Code is more readable as it is written in an object-oriented language and it allows for the use of OOP concepts such as inheritance and polymorphism.  
- The ORM handles the conversion of datatypes from the database to objects and vice versa, thus reducing the mental load of the developer.
- ORMs protect the database from SQL injection attacks, as it will handle the sanitisation of the data before it is sent to the database.

<br>

Example of the object model in the application code:
```
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String)
    price_range = db.Column(db.String)
    cuisine = db.Column(db.String(20), default='tbc')
```
How the data is stored in the database table:

```
 id |        name        | location | price_range | cuisine    
----+--------------------+----------+-------------+----------  
  1 | Mesa Verde         | North    | $           | Mexican
```


---
## R5 Document all endpoints for your API  
### /auth/register/
- Methods: POST  
- Argument: N/A  
- Authentication: N/A  
- Description: allows users to register a new account  
- Request Body:  
```
{
    "username": "newuser12",
    "email": "food@email.com",
    "password": "food123"
}
```
- Return Body:
```
{
    "id": 7,
    "username": "newuser12",
    "email": "food@email.com"
}  
```

### /auth/login/
- Methods: POST  
- Argument: N/A  
- Authentication: N/A  
- Description: users can login to their account  
- Request Body:  
```
{
    "email": "food@email.com",
    "password": "food123"
}
```
- Return Body:  
```
{
    "username": "newuser12",
    "email": "food@email.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODI1MjI3NCwianRpIjoiNjc5NDFjNjUtYjBlYi00YWU0LWFhZGUtNjU4ZmZhMjIxM2Y5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjciLCJuYmYiOjE2NjgyNTIyNzQsImV4cCI6MTY2ODMzODY3NH0.Tjr-azCLWmg_ywPjSkP5e7lHURycF4y25HzrVWPNY18"
}
```

### /auth/users/ 
- Methods: GET  
- Argument: N/A  
- Authentication: registered users with admin privileges  
- Description: users with admin privileges can view all users   
- Request Body: N/A  
- Return Body:  
```
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@email.com",
        "is_admin": true
    },
    {
        "id": 2,
        "username": "user1",
        "email": "user1@email.com",
        "is_admin": false
    },
    {
        "id": 3,
        "username": "user2",
        "email": "user2@email.com",
        "is_admin": false
    },
    ...cont.
```

### /auth/users/\<int:user_id\>
- Methods: GET  
- Argument: user_id (int) e.g '2'  
- Authentication: registered users with admin privileges     
- Description: admin can view a specific user account details  
- Request Body: N/A  
- Return Body:  
```
{
    "id": 2,
    "username": "user1",
    "email": "user1@email.com",
    "is_admin": false,
    "reviews_submitted": [
        {
            "restaurant": {
                "name": "Scopri"
            },
            "rating": 5,
            "date": "2022-11-12",
            "message": "Great food and service"
        }
    ],
    "saved": [
        {
            "restaurant": {
                "name": "Florentino"
            },
            "tag": "To Go"
        }
    ],
    "reviews_count": 1,
    "saved_count": 1
}
```

### /auth/users/\<int:user_id\>
- Methods: DELETE  
- Argument: user_id (int) e.g '2'  
- Authentication: registered users with admin privileges  
- Description: users with admin privileges can delete a user account
- Request Body: N/A  
- Return Body:  
```
{
    "message": "User user3 with id 4 has been deleted"
}
```






### /restaurants/
- Methods: GET  
- Argument: N/A  
- Authentication: N/A  
- Description: Returns all restaurants in the database  
- Request Body: N/A  
- Return Body:  
```
[
    {
        "id": 9,
        "name": "Agostino",
        "region": "North",
        "price_range": "$$",
        "cuisine": "Italian",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 4,
        "name": "Bodega Underground",
        "region": "North",
        "price_range": "$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 3,
        "name": "Florentino",
        "region": "West",
        "price_range": "$$$",
        "cuisine": "Italian",
        "avg_rating": 3.33,
        "saved_for_later": 1
    },
    ...cont.
```  

### /restaurants/\<int:restaurant_id\>
- Methods: GET  
- Argument: restaurant_id (int) e.g '10'  
- Authentication: registered users  
- Description: registered users can request a restaurant of a given id, with more details such as reviews  
- Request Body: N/A  
- Return Body:  
```
{
    "id": 2,
    "name": "Minamishima",
    "location": "East",
    "price_range": "$$",
    "cuisine": "Japanese",
    "avg_rating": 1.0,
    "reviews": [
        {
            "id": 4,
            "user": {
                "id": 5,
                "username": "user4"
            },
            "rating": 1,
            "message": "This place is great!",
            "date": "2022-10-01"
        },
        {
            "id": 5,
            "user": {
                "id": 3,
                "username": "user2"
            },
            "rating": 1,
            "message": "Fantastic food and service!",
            "date": "2022-11-11"
        },
        {
            "id": 6,
            "user": {
                "id": 4,
                "username": "user3"
            },
            "rating": 1,
            "message": "Good but not great.",
            "date": "2022-10-01"
        }
    ],
    "saved_for_later": 0,
    "tagged_to_go": 0,
    "tagged_fave": 0
}
```  

### /restaurants/cuisine/\<cuisine\>
- Methods: GET  
- Argument: cuisine (string). e.g 'mexican'  
- Authentication: N/A  
- Description: returns all restaurants of a given cuisine  
- Request Body: N/A  
- Return Body:  
```
[
    {
        "id": 4,
        "name": "Bodega Underground",
        "location": "North",
        "price_range": "$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 7,
        "name": "Village Cantina",
        "location": "East",
        "price_range": "$$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    }
]
```  

### /restaurants/location/\<location\>
- Methods: GET  
- Argument: location (string). e.g 'north'  
- Authentication: N/A  
- Description: returns all restaurants of a given location  
- Request Body: N/A  
- Return Body:  
```
[
    {
        "id": 9,
        "name": "Agostino",
        "location": "North",
        "price_range": "$$",
        "cuisine": "Italian",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 4,
        "name": "Bodega Underground",
        "location": "North",
        "price_range": "$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 1,
        "name": "Mesa Verde",
        "location": "North",
        "price_range": "$",
        "cuisine": "Mexican",
        "avg_rating": 5.0,
        "saved_for_later": 1
    },
    {
        "id": 6,
        "name": "Scopri",
        "location": "North",
        "price_range": "$",
        "cuisine": "Italian",
        "avg_rating": 3.33,
        "saved_for_later": 0
    }
]
```  
 
### /restaurants/price/\<sort\>
- Methods: GET  
- Argument: sort (string). e.g 'low'  
- Authentication: N/A  
- Description: returns all restaurants sorted by price range depending on the argument (high/low)  
- Request Body:  N/A  
- Return Body:  
```
[
    {
        "id": 7,
        "name": "Village Cantina",
        "location": "East",
        "price_range": "$$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 5,
        "name": "Nobu",
        "location": "South",
        "price_range": "$$$",
        "cuisine": "Japanese",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    {
        "id": 3,
        "name": "Florentino",
        "location": "West",
        "price_range": "$$$",
        "cuisine": "Italian",
        "avg_rating": 3.33,
        "saved_for_later": 2
    },
    {
        "id": 4,
        "name": "Bodega Underground",
        "location": "North",
        "price_range": "$$",
        "cuisine": "Mexican",
        "avg_rating": 3.33,
        "saved_for_later": 0
    },
    ...cont.
``` 
 
### /restaurants/submit/
- Methods: POST  
- Argument: N/A  
- Authentication: registered users  
- Description: allows registered users to submit a new restaurant to the database  
- Request Body:  
```
{
    "name": "Shake Shack",
    "location": "North",
    "price_range": "$",
    "cuisine": "Burgers",
}
```  
- Return Body:  
```
{
    "id": 18,
    "name": "Shake Shack",
    "location": "North",
    "price_range": "$",
    "cuisine": "Burgers"
}
```  

### /restaurants/\<int:restaurant_id\>
- Methods: PUT, PATCH  
- Argument: restaurant_id (int) e.g '1'  
- Authentication: registered users  
- Description: registered users can change details of a restaurant  
- Request Body:  
```
{
    "name": "Updated Name",
    "location": "North",
    "cuisine": "Updated Name",
    "price_range": "$"
}
```
- Return Body:  
```
{
    "id": 1,
    "name": "Updated Name",
    "location": "North",
    "price_range": "$",
    "cuisine": "Updated Name"
}
```
 
### /restaurants/\<int:restaurant_id\>
- Methods: DELETE  
- Argument: restaurant_id (int)  
- Authentication: registered users with admin privileges  
- Description: admin can delete a restaurant from the database  
- Request Body: N/A  
- Return Body:
```
{
    "message": "Restaurant 'Scopri' with id '6' deleted successfully"
}
```  
  
### /restaurants/\<int:restaurant_id\>/review
- Methods: POST  
- Argument: restaurant_id (int) e.g '2'  
- Authentication: registered users  
- Description: registered users can submit a review for a restaurant  
- Request Body:  
```
{
    "rating": "5",
    "message": "Great food and service"
}
``` 
- Return Body:  
```
{
    "id": 38,
    "restaurant": {
        "name": "Bodega Underground"
    },
    "date": "2022-11-12",
    "rating": 5,
    "message": "Great food and service",
    "user": {
        "id": 1,
        "username": "admin"
    }
}
```  
 
### /restaurants/\<int:restaurant_id\>/review
- Methods: PUT, PATCH  
- Argument: restaurant_id (int) e.g '2'  
- Authentication: registered users  
- Description: registered users can edit their review for a restaurant  
- Request Body:  
```
{
    "rating": "4",
    "message": "Updated review"
}
```
- Return Body:  
```
{
    "id": 11,
    "restaurant": {
        "name": "Bodega Underground"
    },
    "date": "2022-11-12",
    "rating": 4,
    "message": "Updated review",
    "user": {
        "id": 3,
        "username": "user2"
    }
}
```
 
### /restaurants/\<int:restaurant_id\>/review
- Methods: DELETE   
- Argument: restaurant_id (int) e.g '2'  
- Authentication: registered users  
- Description: registered users can delete their review for a restaurant  
- Request Body: N/A  
- Return Body:  
```
{
    "message": "Review for restaurant 'Minamishima' with id '2' deleted successfully"
}
```
 
### /restaurants/\<int:restaurant_id\>/save
- Methods: POST   
- Argument: restaurant_id (int) e.g '2'  
- Authentication: registered users  
- Description: registered users can save a restaurant to a list with a tag  
- Request Body:
```
{
    "tag": "To Go"
}
```  
- Return Body:  
```
{
    "message": "Restaurant 'Florentino' has been added to your saved restaurants list successfully"
}
```

 
### /restaurants/\<int:restaurant_id\>/save
- Methods: PUT,PATCH  
- Argument: restaurant_id (int) e.g '2'
- Authentication: registered users  
- Description: registered users can edit the tag of a restaurant in their saved list.
- Request Body:  
```
{
    "tag": "Fave"
}
```
- Return Body:  
```
{
    "message": "Tag for saved restaurant with id '3' updated successfully"
}
```  
 
### /restaurants/\<int:restaurant_id\>/save
- Methods: DELETE  
- Argument: restaurant_id (int) e.g '3'  
- Authentication: registered users  
- Description: registered users can delete a restaurant from their saved list.
- Request Body: N/A
- Return Body:
```
{
    "message": "Restaurant 'Florentino' with id '3' deleted successfully"
}
```

### /profile/
- Methods: GET  
- Argument: N/A  
- Authentication: registered users  
- Description: registered users can view their profile with details of their saved restaurants and reviews
- Request Body: N/A  
- Return Body:  
```
{
    "id": 2,
    "username": "user1",
    "email": "user1@email.com",
    "reviews_count": 1,
    "saved_count": 1
}
```
 
### /profile/saved/
- Methods: GET  
- Argument: N/A  
- Authentication: registered users  
- Description: registered users can view their saved restaurants list
- Request Body: N/A  
- Return Body:  
```
[
    {
        "id": 5,
        "restaurant": {
            "name": "Florentino"
        },
        "tag": "To Go"
    },
    {
        "id": 6,
        "restaurant": {
            "name": "Bodega Underground"
        },
        "tag": "Fave"
    }
]
```
 
### /profile/saved/\<saved_id\>
- Methods: DELETE  
- Argument: saved_id (int) e.g '5'  
- Authentication: registered users  
- Description: registered users can delete a restaurant from their saved list
- Request Body: N/A  
- Return Body:  
```
{
    "message": "Saved restaurant 5 deleted"
}
```
 
### /profile/reviews/
- Methods: GET  
- Argument: N/A  
- Authentication: registered users  
- Description: registered users can view a list of their submitted reviews
- Request Body: N/A   
- Return Body:  
```
[
    {
        "id": 28,
        "restaurant": {
            "name": "Scopri"
        },
        "date": "2022-11-12",
        "rating": 5,
        "message": "Great food and service"
    }
]
```
 
### /profile/reviews/\<review_id\>
- Methods: DELETE  
- Argument: review_id (int) e.g '28'  
- Authentication: registered users  
- Description: registered users can delete a review they have submitted  
- Request Body: N/A   
- Return Body:
```
{
    "message": "Review with id '28' deleted successfully"
}
```


 ---
## R6 An ERD for your app  
![Entity Relationship Diagram](/docs/ERD.jpeg)

---
## R7 Detail any third party services that your app will use  

<b>Flask</b> - Python framework used to create wbe applications.  
<b>Blueprint</b> - Flask extension for modular applications, by creating template routes for the application.  
<b>flask-SQLAlchemy</b> - ORM , used to create models for the database.  
<b>psychopg2</b> - PostgreSQL adapter for python, it is used by SQLAlchemy to send SQL queries to the database.  
<b>Marshmallow</b> - a library used for validating, serializing and deserializing data.  
<b>Bcrypt</b> - a library used for hashing passwords, before storing them in the database.  
<b>flask_jwt_extended</b> - JWT authentication  
<b>JWTManger</b> - JSON Web Token Manager, used to create and verify tokens.  
<b>Datetime</b> - Python library used for the correct formatting of dates and times.  



---
## R8 Describe your projects models in terms of the relationships they have with each other
This project consisted of 4 tables: <b>User, Restaurants, Reviews, Saved </b> . 

<b>User Model</b>: this model will store all the information regarding a user who is registered to use the app. This includes the user's username, email, password and a list of reviews and saved restaurants.  

The user model has a one to many relationship with the reviews and saved models. This means that a user can have many reviews and saved restaurants, but a review or saved restaurant can only belong to one user.  

The one to many relationship is created by the back_populates argument seen below. This allows for data from the associated child table to be accessed from the parent Users table.

```
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reviews_submitted = db.relationship('Review', back_populates='user', cascade='all, delete')
    saved = db.relationship('Saved', back_populates='user', cascade='all, delete')
```
<b>Restaurant Model</b>: this model will store all the information regarding a restaurant. This includes the restaurant's name, location, cuisine type, price range and a list of reviews.  

The restaurant model has a one to many relationship with the reviews and saved models. This means that a restaurant can have many reviews and be saved to many users profiles, but a review or save can only belong to one restaurant.  

When the restaurant model is displayed it will query the associated child table (reviews and saved) and returns the data in a list along with the restaurant data.
```
class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String)
    price_range = db.Column(db.String)
    cuisine = db.Column(db.String(20), default='tbc')
    
    reviews = db.relationship('Review', back_populates='restaurant', cascade='all, delete')
    saved = db.relationship('Saved', back_populates='restaurant', cascade='all, delete')

```

<b>Saved Model</b>: this model will store all the information regarding a saved restaurant for when a user would like to add the restaurant to a list for later reference. This includes the restaurant's id, user's id and a tag. The tag is used to categorise the saved restaurant. For example, a user may want to save a restaurant to their profile to go to later, or they may want to save a restaurant as a favourite. The tag is used to differentiate between the two.

The saved model has a many to one relationship with the user and restaurant models. This means that a saved restaurant can only belong to one user and one restaurant, but a user or restaurant can have many saved restaurants.  

When a restaurant is added to the saved table, the id of the restaurant and the user is stored in the table. This allows for the restaurant to be accessed from the user's profile. This is facilitated by the foreign key argument seen below. This allows for the data from the associated parent table to be accessed from the child table.


```
class Saved(db.Model):
    __tablename__ = 'saved'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), nullable=True, default='')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)


    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='saved')
    restaurant = db.relationship ("Restaurant", back_populates='saved')
```



<b>Review Model</b>: this model stores all the information regarding a review submitted by a user. This includes the restaurant's id, user's id, date, rating and message. The date is automatically generated when the review is submitted. The rating is a number between 1 and 5, and the message is a string of text.  

The review model has a many to one relationship with the user and restaurant models. This means that a review can only belong to one user and one restaurant, but a user or restaurant can have many reviews.   

When a new review is stored in the table, the user id and restaurant id are used to query the associated user and restaurant tables. The data from the user and restaurant tables are then stored in the review table. This allows for the data to be displayed when the review is queried.  

This is facilitated by the foreign key argument seen below. This allows for the data from the associated parent table to be accessed from the child table.
```
class Review(db.Model):
    __tablename__ = 'reviews' #table name used for db

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    rating = db.Column(db.Integer,)
    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # stores all fields from User table into user object
    user = db.relationship ("User", back_populates='reviews_submitted')
    restaurant = db.relationship ("Restaurant", back_populates='reviews')
    
```

---
## R9 Discuss the database relations to be implemented in your application  

The main tables in the database are the Users and Restaurants tables. They data stored in those tables are all unique, as there can only be one user with a specific username and email. The same applies to the restaurant table, as there can only be one restaurant with a specific name and location.  
In addition to the above tables, there are also tables for Reviews and Saved restaurants. As the data in these tables relate to the a single restaurant, they are considered children tables. The data in these tables are accessed from the parent tables.  

From the ERD it can be seen that the Restaurant table has a one to many relationship with the reviews and saved tables. This means that a restaurant can have many reviews and be saved to many users profiles, but a review or save can only belong to one restaurant.  
Similary the User table has a one to many relationship with the reviews and saved tables indicating that a user can have many reviews and saved restaurants, but a review or save can only belong to one user.  

In the Reviews and Saved tables, the user and restaurant id, stored along with the reviews and saved data, and are used to retrieve the data from the associated parent tables. This allows for the data to be displayed when the review or saved restaurant is queried.


---
## R10 Describe the way tasks are allocated and tracked in your project  
The project was managed using Trello's Kanban board system, where tasks are broken down into small chunks and their progress moved along the board. The board is broken down into columns and updated when a task is completed. 

[Trello Board](https://trello.com/b/3Zt5Nzh5/t2a2)





---
## Getting Started 
### Database
Start PSQL
```
psql
```
Create the database
```
create database food_finder;
```
Create new user
```
create user db_dev with password 'password123';
```
Grant all privileges
```
grant all privileges on database food_finder to db_dev;
```
### Virtual Environment
Create new virtual environment  
```
python3 -m venv .venv
```
Activate the virtual environment  
```
source .venv/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
### Flask
Start Flask
```
flask run
```
Seed the database
```
flask db drop && flask db create && flask db seed
```



