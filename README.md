# T2A2 API Webserver  


# R1 Identification of the problem you are trying to solve by building this particular app.  
Like many foodies, I enjoy trying out new restaurants and cuisines. However the amount of restaurants you have to choose from can be overwhelming, and when you have tried the restaurant it is hard to keep track of the ones you like.


# R2 Why is it a problem that needs solving?  
With the cost of living being so high in Australia, it is important to find the best value for money, and making sure every new visit worthwhile. With the app you can find new restaurants submitted by like minded foodies, seeing reviews and ratings. Once you have visited a restaurant you can add your own review and rating. This app will also allow you to save restaurants you like to your account, and keep track of the ones you would like to try and the ones you thought were great.


# R3 Why have you chosen this database system. What are the drawbacks compared to others?  

There are two main types of databases to choose from, relational and 

How it will benefit the project. 
A relational database was chosen for the following reasons: 
- The data within this project will have a consistent structure with and known attributes.
- Entities in the database will query other entities to retrieve data.
- 
As the data being handled comes in a consistent structure it was the ideal solution to use a relational database system

https://www.oracle.com/au/database/what-is-a-relational-database/



For this project the Postgres database.
- about post
- benefits of postgtres
- drawbacks of postgtres



# R4 Identify and discuss the key functionalities and benefits of an ORM  
- What is an ORM
Object Relational Mapping (ORM) is a technique using libraries to represent tables in a relational database as objects in object-oriented programming languages. This allows for CRUD operations to be performed on the database using object-oriented programming languages, such as Python and Javascript.

- Functionalities
-Benefits  
- Allows for creation of dynamic queries. For example a user can search for a restaurant by name, or by cuisine type, or by location. This can be done by creating a dynamic query that will search for the restaurant based on the parameters provided by the user. 

- Code is more readable as it is written in an object-oriented language and it allows for the use of OOP concepts such as inheritance and polymorphism.  

-Drawbacks  
- ORM libraries can be slow as they have to translate the queries into SQL.
- Writing code for complex queries is much more difficult than writing SQL queries.
  


Example of query to retrieve all entries in a table called restaurants
```
@restaurants_bp.route('/')
def get_all_restaurants():
    stmt = db.select(Restaurant)
    restaurants = db.session.scalars(stmt)
    return RestaurantSchema(many=True).dump(restaurants)
```





# R5 Document all endpoints for your API  


### /restaurants/
Methods: GET  
Argument: N/A  
Authentication: N/A  
Description: Returns all restaurants in the database  
Request Body: N/A  
Return Body:  
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
    ...
```  

### /restaurants/\<int:restaurant_id\>
Methods: GET  
Argument: restaurant_id (int) e.g '10'  
Authentication: registered users  
Description: registered users can request a restaurant of a given id, with more details such as reviews  
Request Body: N/A  
Return Body:  
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
Methods: GET  
Argument: cuisine (string). e.g 'mexican'  
Authentication: N/A  
Description: returns all restaurants of a given cuisine  
Request Body: N/A  
Return Body:  
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
Methods: GET  
Argument: location (string). e.g 'north'  
Authentication: N/A  
Description: returns all restaurants of a given location  
Request Body: N/A  
Return Body:  
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
Methods: GET  
Argument: sort (string). e.g 'low'
Authentication: N/A  
Description: returns all restaurants sorted by price range depending on the argument (high/low).
Request Body:  N/A  
Return Body:  
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
Methods: POST  
Argument: N/A  
Authentication: registered users  
Description: allows registered users to submit a new restaurant to the database.  
Request Body:  
```
{
    "name": "Shake Shack",
    "location": "North",
    "price_range": "$",
    "cuisine": "Burgers",
}
```  
Return Body:  
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
Methods: PUT, PATCH
Argument: restaurant_id (int) e.g '1'  
Authentication: registered users  
Description: registered users can change details of a restaurant.
Request Body:  
```
{
    "name": "Updated Name",
    "location": "North",
    "cuisine": "Updated Name",
    "price_range": "$"
}
```
Return Body:  
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
Methods: DELETE
Argument: restaurant_id (int)  
Authentication: registered users with admin access  
Description: admin can delete a restaurant from the database.
Request Body: N/A  
Return Body:
```
{
    "message": "Restaurant 'Scopri' with id '6' deleted successfully"
}
```  
  
### /restaurants/\<int:restaurant_id\>/review
Methods: POST
Argument: restaurant_id (int) e.g '2'  
Authentication: registered users  
Description: registered users can submit a review for a restaurant.
Request Body:  
```
{
    "rating": "5",
    "message": "Great food and service"
}
``` 
Return Body:  
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
Methods: PUT, PATCH
Argument: restaurant_id (int) e.g '2'  
Authentication: registered users  
Description: registered users can edit their review for a restaurant.  
Request Body:  
```
{
    "rating": "4",
    "message": "Updated review"
}
```
Return Body:  
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
Methods: DELETE  
Argument: restaurant_id (int) e.g '2'  
Authentication: registered users  
Description: registered users can delete their review for a restaurant
Request Body: N/A  
Return Body:  
```
{
    "message": "Review for restaurant 'Minamishima' with id '2' deleted successfully"
}
```
 
### /restaurants/\<int:restaurant_id\>/save
Methods: POST  
Argument: restaurant_id (int) e.g '2'  
Authentication: registered users  
Description: registered users can save a restaurant to a list with a tag
Request Body:
```
{
    "tag": "To Go"
}
```  
Return Body:  
```
{
    "message": "Restaurant 'Florentino' has been added to your saved restaurants list successfully"
}
```

 
### /restaurants/\<int:restaurant_id\>/save
Methods: PUT,PATCH  
Argument: restaurant_id (int) e.g '2'
Authentication: registered users  
Description: registered users can edit the tag of a restaurant in their saved list.
Request Body:  
```
{
    "tag": "Fave"
}
```
Return Body:  
```
{
    "message": "Tag for saved restaurant with id '3' updated successfully"
}
```  
 
### /restaurants/\<int:restaurant_id\>/save
Methods: DELETE  
Argument: restaurant_id (int) e.g '3'  
Authentication: registered users  
Description: registered users can delete a restaurant from their saved list.
Request Body: N/A
Return Body:
```
{
    "message": "Restaurant 'Florentino' with id '3' deleted successfully"
}
```


### /auth/register/
Methods: POST  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /auth/login/
Methods: POST  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /auth/users/
Methods: GET  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 

### /auth/users/\<id\>
Methods: GET  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /auth/users/\<id\>
Methods: DELETE  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 




### /profile/
Methods: GET  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /profile/saved/
Methods: GET  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /profile/saved/\<id\>
Methods: DELETE  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /profile/reviews/
Methods: GET  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 
### /profile/reviews/\<id\>
Methods: DELETE  
Argument:  
Authentication:  
Description:  
Request Body:  
Return Body:  
 






## Restaurant routes


### /restaurants/   
Methods: GET  
Arguments:  
Description:  Return all restaurants
Request JSON:  
Return JSON:  

### /restaurants/
Methods: POST  
Arguments:  
Description:  Create a new restaurant  
Request JSON Example:  
```
{
    "name": "Restaurant Name",
    "location": "North",
    "cuisine": "Italian",
    "price_range": "$$"
}
```
Return JSON:
```

```














### /restaurants/\<int:id\>  
Methods: GET  
Arguments:  
Description:  Return a restaurant by id  

### /restaurants/\<int:id\>    
Methods: PUT  
Arguments: 
Description:  Update a restaurant by id  

### /restaurants/\<int:id\>  
Methods: DELETE  
Arguments:  
Description:  Delete a restaurant by id  




## Auth
### /auth/users/
Methods: GET
Arguments:
Description:  Return all users
Request JSON:
Return JSON:
```

```







## profile
### /profile/
Methods: GET
Arguments:
Description:  Returns logged in user profile










Get all restaurants

Post review for a restaurant



## User





## Auth
Sign up


Login











# R6 An ERD for your app  
![Entity Relationship Diagram](/docs/ERD.jpeg)


# R7 Detail any third party services that your app will use  

<b>Flask</b> - Python framework used to create wbe applications. 
<b>Blueprint</b> - Flask extension for modular applications  
<b>jsonify</b> - Flask extension for returning JSON responses  
request - Flask extension for handling HTTP requests  
abort - Flask extension for handling HTTP errors  
<b>SQLAlchemy</b> - ORM , generates SQL statements
<b>psychopg2</b> - PostgreSQL adapter for python, it is used by SQLAlchemy to send SQL queries to the database.
<b>Marshmallow</b> - a library used for validating data, serializing and deserializing data.
    fields - Marshmallow extension for handling data types  
<b>Bcrypt</b> - Password Hashing  
<b>flask_jwt_extended</b> - JWT authentication  
<b>jwt_required</b> -  
<b>get_jwt_identity</b> -   
<b>JWTManger</b> - JSON Web Token Manager  
Datetime - Date and Time  
<b>marshmallow</b>-validate - Validation  
datetime - Date and Time  




# R8 Describe your projects models in terms of the relationships they have with each other  

# R9 Discuss the database relations to be implemented in your application  

# R10 Describe the way tasks are allocated and tracked in your project  
The project managed using Trello's Kanban board system, where tasks are broken down into small chunks and their progress moved along the board. The board is broken down into columns and updated when a task is completed. 


## Installation

create virtual machine  
```
python3 -m venv .venv
```
install requirements  
```
pip install -r requirements.txt
```
create database in psql called food_finder
```
create database food_finder;
```
connect to database  
``` 
\c food_finder
```


replace USERNAME and PASSWORD with your own    


## Overview  
  
## Table Of Contents  

## Database  
pros and cons of using database


## ORM  
Identify and discuss benefits of an ORM
ORM Obejct Relational Mapping

## API Endpoints  


## third party services 


## Entity Relationship Diagram  
  

## Project Models

## Database Relations  



##  Project Management  
explanation of project management tools used  
[Project Trello Board](https://trello.com/b/3Zt5Nzh5/t2a2)

User stories



## References
