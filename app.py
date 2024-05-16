from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Carrera(db.Model):
    _tablename_= 'carrera'

    clavecarrera = db.Column(db.String(13), primary_key=True, nullable=False)
    nombrecarrera = db.Column(db.String(100))
    estructuragenetica = db.Column(db.Integer)

    def json(self):
        return{
            'Clave': self.clavecarrera,
            'Nombre': self.nombrecarrera,
            'Estructura Genetica': self.estructuragenetica
        }
        
class Especialidad(db.Model):
    _tablename_= 'especialidad'

    claveespecialidad = db.Column(db.String(16), primary_key=True, nullable=False)
    nombreespecialidad = db.Column(db.String(100))
    creditos = db.Column(db.Integer)
    clavecarrera = db.Column(db.String(13), db.ForeignKey('carrera.clavecarrera'), nullable=False)

    def json(self):
        return{
            'Clave': self.claveespecialidad,
            'Especialidad': self.nombreespecialidad,
            'Creditos': self.creditos,
            'Carrera': self.clavecarrera
        }
    
class Materia(db.Model):
    _tablename_= 'materia'

    clavemateria = db.Column(db.String(8), primary_key=True, nullable=False)
    nombremateria = db.Column(db.String(100))
    creditos = db.Column(db.Integer)
    semestre = db.Column(db.Integer)
    clavecarrera = db.Column(db.String(13), db.ForeignKey('carrera.clavecarrera'), nullable=False)

    def json(self):
        return{
            'Clave': self.clavemateria,
            'Materia': self.nombremateria,
            'Creditos': self.creditos,
            'Semestre': self.semestre,
            'Carrera': self.clavecarrera
        }
    
class Especial(db.Model):
    _tablename_ = 'materiaespecial'

    claveespecial = db.Column(db.String(8), primary_key=True, nullable=False)
    nombremateria = db.Column(db.String(100))
    creditos = db.Column(db.Integer)
    semestre = db.Column(db.Integer)
    claveespecialidad = db.Column(db.String(16), db.ForeignKey('especialidad.claveespecialidad'), nullable=False)

    def json(self):
        return{
            'Clave': self.claveespecial,
            'Materia': self.nombremateria,
            'Creditos': self.creditos,
            'Semestre': self.semestre,
            'Especialidad': self.claveespecialidad
        }

db.create_all()

@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

#Endpoints para las carreras-------------

@app.route('/carrera', methods=['GET'])
def get_carreras():
    try:
        carreras = Carrera.query.all()
        return make_response(jsonify([carrera.json() for carrera in carreras]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error getting carreras'}), 500)
    

@app.route('/carrera/<id>', methods=['GET'])
def get_carrera(id):
    try:
        carrera = Carrera.query.filter_by(clavecarrera=id).first()
        if carrera:
            return make_response(jsonify({'carrera': carrera.json()}), 200)
        return make_response(jsonify({'message': 'carrera not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error getting carrera'}), 500)


@app.route('/carrera', methods=['POST'])
def add_carrera():
    try:
        data = request.get_json()
        new_carrera = Carrera(
            clavecarrera = data['Clave'],
            estructuragenetica = int(data['Estructura Genetica']),
            nombrecarrera = data['Nombre'])
        db.session.add(new_carrera)
        db.session.commit()
        return make_response(jsonify({'message': 'carrera created'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creating carrera'}), 500)


@app.route('/carrera/<id>', methods=['PUT'])
def update_carrera(id):
    try:
        carrera = Carrera.query.filter_by(clavecarrera=id).first()
        if carrera:
            data = request.get_json()
            carrera.nombrecarrera = data['Nombre']
            carrera.estructuragenetica = int(data['Estructura Genetica'])
            db.session.commit()
            return make_response(jsonify({'message': 'carrera updated'}), 200)
        return make_response(jsonify({'message': 'carrera not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error updating carrera'}), 500)


@app.route('/carrera/<id>', methods=['DELETE'])
def delete_carrera(id):
    try:
        carrera = Carrera.query.filter_by(clavecarrera=id).first()
        if carrera:
            db.session.delete(carrera)
            db.session.commit()
            return make_response(jsonify({'message': 'carrera deleted'}), 200)
        return make_response(jsonify({'message': 'carrera not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error deleting carrera'}), 500)

#Endpoints para las especialidades

@app.route('/especialidades', methods=['GET'])
def get_especialidades():
    try:
        especialidades = Especialidad.query.all()
        return make_response(jsonify([especialidad.json() for especialidad in especialidades]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error getting especialidades'}), 500)
    
@app.route('/especialidad/<id>', methods=['GET'])
def get_especialidad(id):
    try:
        especialidad = Especialidad.query.filter_by(claveespecialidad=id).first()
        if especialidad:
            return make_response(jsonify({'especialidad': especialidad.json()}), 200)
        return make_response(jsonify({'message': 'especialidad not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error getting especialidad'}), 500)

@app.route('/especialidad', methods=['POST'])
def add_especialidad():
    try:
        data = request.get_json()
        new_especialidad = Especialidad(
            claveespecialidad = data['Clave'],
            nombreespecialidad = data['Especialidad'],
            creditos = int(data['Creditos']),
            clavecarrera = data['Carrera']
        )
        db.session.add(new_especialidad)
        db.session.commit()
        return make_response(jsonify({'message': 'especialidad created'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creating especialidad'}), 500)


@app.route('/especialidad/<id>', methods=['PUT'])
def update_especialidad(id):
  try:
    especialidad = Especial.query.filter_by(claveespecialidad=id).first()
    if especialidad:
        data = request.get_json()
        especialidad.nombreespecialidad = data['Especialidad']
        especialidad.creditos = int(data['Creditos'])
        especialidad.clavecarrera = data['Carrera']
        db.session.commit()
        return make_response(jsonify({'message': 'especialidad updated'}), 200)
    return make_response(jsonify({'message': 'especialidad not found'}), 404)
  except Exception:
    return make_response(jsonify({'message': 'error updating especialidad'}), 500)


@app.route('/especialidad/<id>', methods=['DELETE'])
def delete_especialidad(id):
    try:
        especialidad = Especialidad.query.filter_by(claveespecialidad=id).first()
        if especialidad:
            db.session.delete(especialidad)
            db.session.commit()
            return make_response(jsonify({'message': 'especialidad deleted'}), 200)
        return make_response(jsonify({'message': 'especialidad not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error deleting especialidad'}), 500)


#Endpoints para las materias

@app.route('/materias', methods=['GET'])
def get_materias():
    try:
        materias = Materia.query.all()
        return make_response(jsonify([materia.json() for materia in materias]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error getting materias'}), 500)
    
@app.route('/materia/<id>', methods=['GET'])
def get_materia(id):
    try:
        materia = Materia.query.filter_by(clavemateria=id).first()
        if materia:
            return make_response(jsonify({'materia': materia.json()}), 200)
        return make_response(jsonify({'message': 'materia not found'}), 404)
    except Exception:
            return make_response(jsonify({'message': 'error getting materia'}), 500)



@app.route('/materia', methods=['POST'])
def add_materia():
    try:
        data = request.get_json()
        new_materia = Materia(
            clavemateria = data['Clave'],
            nombremateria = data['Materia'],
            creditos = int(data['Creditos']),
            semestre = int(data['Semestre']),
            clavecarrera = data['Carrera'])
        db.session.add(new_materia)
        db.session.commit()
        return make_response(jsonify({'message': 'materia created'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creating materia'}), 500)


@app.route('/materia/<id>', methods=['PUT'])
def update_materia(id):
    try:
        materia = Materia.query.filter_by(clavemateria=id).first()
        if materia:
            data = request.get_json()
            materia.nombremateria = data['Materia']
            materia.creditos = int(data['Creditos'])
            materia.semestre = int(data['Semestre'])
            materia.clavecarrera = data['Carrera']
            db.session.commit()
            return make_response(jsonify({'message': 'materia updated'}), 200)
        return make_response(jsonify({'message': 'materia not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error updating materia'}), 500)

@app.route('/materia/<id>', methods=['DELETE'])
def delete_materia(id):
    try:
        materia = Materia.query.filter_by(clavemateria=id).first()
        if materia:
            db.session.delete(materia)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error deleting user'}), 500)

#Endpoints para las materias de especialidad

@app.route('/matesp', methods=['GET'])
def get_especiales():
    try:
        especiales = Especial.query.all()
        return make_response(jsonify([especial.json() for especial in especiales]), 200)
    except Exception:
        return make_response(jsonify({'message': 'error getting materias'}), 500)
    
@app.route('/matesp/<id>', methods=['GET'])
def get_especial(id):
    try:
        especial = Especial.query.filter_by(claveespecial=id).first()
        if especial:
            return make_response(jsonify({'especial': especial.json()}), 200)
        return make_response(jsonify({'message': 'materia not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error getting materia'}), 500)


@app.route('/matesp/add', methods=['POST'])
def add_especial():
    try:
        data = request.get_json()
        new_especial = Especial(
            claveespecial = data['Clave'],
            nombremateria = data['Materia'],
            creditos = int(data['Creditos']),
            semestre = int(data['Semestre']),
            claveespecialidad = data['Especialidad'])
        db.session.add(new_especial)
        db.session.commit()
        return make_response(jsonify({'message': 'materia created'}), 201)
    except Exception:
        return make_response(jsonify({'message': 'error creating materia'}), 500)
    

@app.route('/matesp/<id>', methods=['PUT'])
def update_especial(id):
    try:
        especial = Especial.query.filter_by(claveespecial=id).first()
        if especial:
            data = request.get_json()
            especial.nombremateria = data['Materia']
            especial.creditos = int(data['Creditos'])
            especial.semestre = int(data['Semestre'])
            especial.claveespecialidad = data['Especialidad']
            db.session.commit()
            return make_response(jsonify({'message': 'materia updated'}), 200)
        return make_response(jsonify({'message': 'materia not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error updating materia'}), 500)


@app.route('/matesp/<id>', methods=['DELETE'])
def delete_especial(id):
    try:
        especial = Especial.query.filter_by(claveespecial=id).first()
        if especial:
            db.session.delete(especial)
            db.session.commit()
            return make_response(jsonify({'message': 'materia deleted'}), 200)
        return make_response(jsonify({'message': 'materia not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error deleting materia'}), 500)