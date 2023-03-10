import os
from pymongo import MongoClient, errors, ASCENDING

client: MongoClient = MongoClient(os.getenv("MONGO_URI"))
db = client['students']

db.students.create_index([("student_id", ASCENDING)], unique=True)


def add(student=None):
    res = db.students.find_one({"first_name": student.first_name,
                                "last_name": student.last_name})

    if res:
        return 'name already exists', 409

    if not student.student_id:
        student.student_id = 0

    try:
        doc_id = db.students.insert_one(student.to_dict()).inserted_id
        return student.student_id
    except errors.DuplicateKeyError:
        student.student_id = student.student_id + 1
        return add(student)


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
