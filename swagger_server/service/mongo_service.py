import os
from pymongo import MongoClient
from bson.objectid import ObjectId

client: MongoClient = MongoClient(os.getenv("MONGO_URI"))
db = client['students']


def add(student=None):
    res = db.students.find_one({"first_name": student.first_name,
                                "last_name": student.last_name})

    if res:
        return 'already exists', 409

    count = db.students.count_documents({})
    student.student_id = count
    db.students.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = db.students.find_one({'student_id': student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    student['_id'] = str(student['_id'])
    return student


def delete(student_id=None):
    student = db.students.delete_one({'student_id': student_id})
    if not student.deleted_count:
        return 'not found', 404
    return student_id
