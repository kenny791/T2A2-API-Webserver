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
    "region": "North",
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



#







Get all restaurants

Post review for a restaurant



## User





## Auth
Sign up


Login











# R6 An ERD for your app  





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
