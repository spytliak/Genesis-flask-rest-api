# Genesis-flask-rest-api
The repository is for Genesis DevOps School. 

### Description
The repo is for creating a RESTful API based on Python, Flask and MySQL.  
The database and its structure are created by the application at startup. The application gets the connection parameters to the DBMS from the environment variables.  
Need to create .env file for using app. 

* [app](/app/)                                  - the application folder (flask)
* [api.py](/app/api.py)                         - the application script
* [api_doc.json](/app/api_doc.json)             - the API documentation
* [requirements.txt](requirements.txt)          - the packages that the project requires
* [.env.example](.env.example)                  - the example .env file
* [Dockerfile](Dockerfile)                      - Dockerfile for api
* [docker-compose.yml](docker-compose.yml)      - Docker Compose file

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
 - /api/students/delete/<id> (DELETE) 200        - deleting students data by id
 - /api/health-check/ok (GET)  200               - ok health-check endpoint
 - /api/health-check/bad (GET) 500               - bad health-check endpoint

#### Prerequisites:
For virtualenv:  
   - Python 3
   - MySQL with created user
   - venv, pip packages

For docker:  
   - docker >= 19.03.0
   - docker-compose >= 1.29.0
#### Build the project:
Virtualenv:
```
python3 -m venv venv
source vevn/bin/activate
pip install -r requirements.txt
python3 ./app/api.py
```
Docker-compose:
```
sudo docker-compose build
sudo docker-compose up -d
```

#### Examples using api in console:
Create student:
```
sepy0416@WS-17690:~$ curl -X POST http://127.0.0.1:5000/api/students/add -H 'Content-Type: application/json' -d '{"name":"Dev Ops","email":"devops@mail.com","age":"30","cellphone":"0631230777"}'
{
  "age": 30,
  "cellphone": "0631230777",
  "email": "devops@mail.com",
  "id": 23,
  "name": "Dev Ops"
}
```
Get student, who is not existed in database:
```
sepy0416@WS-17690:~$ curl -X GET http://127.0.0.1:5000/api/students/get/21
{
  "message": "The student with the given ID:21 is not in the database"
}
```
Get student, who is existed in database:
```
sepy0416@WS-17690:~$ curl -X GET http://127.0.0.1:5000/api/students/get/23
{
  "age": 30,
  "cellphone": "0631230777",
  "email": "devops@mail.com",
  "id": 23,
  "name": "Dev Ops"
}
```
Modify age:
```
sepy0416@WS-17690:~$ curl -X PATCH http://127.0.0.1:5000/api/students/modify/23 -H 'Content-Type: application/json' -d '{"age": "31"}'
{
  "age": 31,
  "cellphone": "0631230777",
  "email": "devops@mail.com",
  "id": 23,
  "name": "Dev Ops"
}
```
Change all params:
```
sepy0416@WS-17690:~$ curl -X PUT http://127.0.0.1:5000/api/students/change/23 -H 'Content-Type: application/json' -d '{"name":"Git Ops","email":
"gitops@mail.com","age":"32","cellphone":"0637777777"}'
{
  "age": 32,
  "cellphone": "0637777777",
  "email": "gitops@mail.com",
  "id": 23,
  "name": "Git Ops"
}
```
Remove student:
```
sepy0416@WS-17690:~$ curl -X DELETE http://127.0.0.1:5000/api/students/delete/23
{
  "message": "Student with the given ID:23 was deleted"
}
```

#### The test changing api (docker volume):
Check volumes:
```
sepy0416@WS-17690:~$ sudo docker volume ls
DRIVER    VOLUME NAME
local     genesis-flask-rest-api_api-db
local     genesis-flask-rest-api_flaskapi
```
The genesis-flask-rest-api_flaskapi volume is for flask api.  
Check mountpoint:
```
sepy0416@WS-17690:~$ sudo docker volume inspect genesis-flask-rest-api_flaskapi |grep -i 'mount'
        "Mountpoint": "/var/lib/docker/volumes/genesis-flask-rest-api_flaskapi/_data",
```
Change return endpoints '/':
```
sepy0416@WS-17690:~$ sudo sed -i 's/Hello from students API!/Genesis API!/g' /var/lib/docker/volumes/genesis-flask-rest-api_flaskapi/_data/api.py
```
Check api:
```
sepy0416@WS-17690:~$ sudo curl -X GET http://127.0.0.1:5000/
<p>Genesis API!</p>
```