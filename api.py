from asyncio.proactor_events import _ProactorBasePipeTransport
import os
import json
 
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from marshmallow import Schema, fields
 
dotenv.load_dotenv()
 
db_user = os.environ.get('DB_USERNAME')
db_pass = os.environ.get('DB_PASSWORD')
db_hostname = os.environ.get('DB_HOSTNAME')
db_name = os.environ.get('DB_NAME')
 
DB_URI = 'mysql+pymysql://{db_username}:{db_password}@{db_host}/{database}'.format(db_username=db_user, db_password=db_pass, db_host=db_hostname, database=db_name)
 
engine = create_engine(DB_URI, echo=True)
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cellphone = db.Column(db.String(13), unique=True, nullable=False)
 
    @classmethod
    def get_all(cls):
        return cls.query.all()
 
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
 
    def save(self):
        db.session.add(self)
        db.session.commit()
 
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
 
class StudentSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()
    age = fields.Integer()
    cellphone = fields.Str()
 
@app.route('/', methods = ['GET'])
def home():
    """Home endpoint"""
    return '<p>Hello from students API!</p>', 200
 
@app.route('/api', methods = ['GET'])
def api_main():
    """Main endpoint"""
    with open('api_doc.json', 'r', encoding='utf-8') as j:
        json_data = json.load(j)
    return jsonify(json_data), 200
 
@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Get all students endpoint"""
    students = Student.get_all()
    student_list = StudentSchema(many=True)
    response = student_list.dump(students)
    return jsonify(response), 200
 
@app.route('/api/students/get/<int:id>', methods = ['GET'])
def get_student(id):
    """Get student endpoint"""
    student_info = Student.query.filter(Student.id == id).one_or_none()
    if student_info:
        serializer = StudentSchema()
        response = serializer.dump(student_info)
        return jsonify(response), 200
    else:
        return jsonify('The student with the given ID:{} is not in the database'.format(id)), 404
 
@app.route('/api/students/add', methods = ['POST'])
def add_student():
    """Add new student endpoint"""
    json_data = request.get_json()
    new_student = Student(
        name= json_data.get('name'),
        email=json_data.get('email'),
        age=json_data.get('age'),
        cellphone=json_data.get('cellphone')
    )
    new_student.save()
    serializer = StudentSchema()
    data = serializer.dump(new_student)
    return jsonify(data), 201

@app.route('/api/students/modify/<int:id>', methods = ['PATCH'])        # PATCH => Partially update an existing resource (not all attributes required).
def modify_student(id):
   """Modify student endpoint"""
   if request.method == 'PATCH':
        # JSONify request details
        json_data = request.get_json()
        # check data
        if not json_data:
            return jsonify('No data provided'), 400
       # get requested id object, used one_or_none for check if the row is not exist
        student_modify = Student.query.filter(Student.id == id).one_or_none()
        if student_modify:
            # check objects
            if "name" in json_data:
                student_modify.name = json_data.get('name')
            if "email" in json_data:
                student_modify.email = json_data.get('email')
            if "age" in json_data:
                student_modify.age = json_data.get('age')
            if "cellphone" in json_data:
                student_modify.cellphone = json_data.get('cellphone')
            # update data, created 'def update()' for that
            student_modify.update()
            serializer = StudentSchema()
            data = serializer.dump(student_modify)
            return jsonify(data), 201
        else:
            return jsonify('The student with the given ID:{} is not in the database'.format(id)), 404

@app.route('/api/students/change/<int:id>', methods = ['PUT'])         # PUT => Set all new attributes for an existing resource.
def change_student(id):
    """Change student endpoint"""
    if request.method == 'PUT':
        # get requested id object
        student_change = Student.query.filter(Student.id == id).one_or_none()
        if student_change:
            # JSONify request details
            json_data = request.get_json()
            student_change.name = json_data.get('name')
            student_change.email = json_data.get('email')
            student_change.age = json_data.get('age')
            student_change.cellphone = json_data.get('cellphone')
            
            # check all objects, needed for PUT if some object is missing
            try: 
                # update data
                student_change.update()
                serializer = StudentSchema()
                data = serializer.dump(student_change)
                return jsonify(data), 201
            except Exception as e:
                return ("Error: " + str(e)), 400    # example: "Error: (pymysql.err.IntegrityError) (1048, "Column 'cellphone' cannot be null")"

        else:
            return jsonify('The student with the given ID:{} is not in the database'.format(id)), 404

@app.route('/api/students/delete/<int:id>', methods = ['DELETE'])
def delete_student(id):
    """Remove student endpoint"""
    if request.method == 'DELETE':
        # get requested id object
        delete_student = Student.query.filter(Student.id == id).one_or_none()
        if delete_student:
            delete_student.delete()
            return jsonify('Student with the given ID:{} was deleted'.format(id)), 204
        else:
            return jsonify('The student with the given ID:{} is not in the database'.format(id)), 404

@app.route('/api/health-check/ok', methods = ['GET'])
def health_check_ok():
    """Healthy endpoint - OK"""
    return jsonify('Health check is OK'), 200

@app.route('/api/health-check/bad', methods = ['GET'])
def health_check_bad():
    """Healthy endpoint - BAD"""
    return jsonify('Health check is BAD'), 500
 
if __name__ == '__main__':
    if not database_exists(engine.url):
        create_database(engine.url)
    db.create_all()
    app.run(use_reloader=True, debug=True)