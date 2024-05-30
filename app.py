from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index_number = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'index_number': self.index_number,
            'name': self.name,
            'points': self.points
        }

@app.route('/student/<index_number>', methods=['GET'])
def get_student_points(index_number):
    student = Student.query.filter_by(index_number=index_number).first()
    if student:
        return jsonify(student.to_dict())
    return jsonify({'message': 'Student not found'}), 404

@app.route('/admin/add_points', methods=['POST'])
def add_points():
    data = request.get_json()
    index_number = data.get('index_number')
    points = data.get('points')
    
    student = Student.query.filter_by(index_number=index_number).first()
    if student:
        student.points += points
        db.session.commit()
        return jsonify({'message': 'Points added successfully', 'student': student.to_dict()})
    return jsonify({'message': 'Student not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

@app.route('/packages')
def list_packages():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    packages = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    return jsonify(packages)
