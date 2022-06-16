# Genesis-flask-rest-api
The repository is for Genesis DevOps School. 

### Description
The repo is for creating a RESTful API based on Python, Flask and MySQL.  
The database and its structure are created by the application at startup. The application gets the connection parameters to the DBMS from the environment variables.  

* [requirements.txt](requirements.txt)     - the packages that the project requires
* [api.py](api.py)                         - the application script
* [api_doc.json](api_doc.json)             - the API documentation

The api database will have a student table with fields:  
 - id (int, unique, autoincrement)
 - name (str)
 - email (str)
 - age (int)
 - cellphone (str)

The key endpoints:
 - /api (GET) 200                                - root endpoint
 - /api/students (GET) 200                       – getting a list of students
 - /api/students/get/<id> (GET) 200              – getting students data by id
 - /api/students/add (POST) 201                  – adding a student to the list
 - /api/students/modify/<id> (PATCH) 201         - modifying students data by id
 - /api/students/change/<id> (PUT) 201           - changing students data by id
 - /api/students/delete/<id> (DELETE) 204        - deleting students data by id
 - /api/health-check/ok (GET)  200               - ok health-check endpoint
 - /api/health-check/bad (GET) 500               - bad health-check endpoint

#### Prerequisites:
   - Python 3
   - MySQL with created user
   - venv, pip packages

#### Build the project:
```
python3 -m venv venv
source vevn/bin/activate
pip install -r requirements.txt
```

#### Run API:
```
python3 api.py
```
