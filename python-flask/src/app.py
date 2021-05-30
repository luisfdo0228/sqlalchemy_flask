from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/matriculateBD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Acudiente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(70), unique=True)
    apellidos = db.Column(db.String(100))
    documento = db.Column(db.String(20))
    direccion = db.Column(db.String(60))
    municipio = db.Column(db.String(40))
    ocupacion = db.Column(db.String(60))
    parentesco = db.Column(db.String(20))
    num1 = db.Column(db.String(15))
    num2 = db.Column(db.String(15))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))

    def __init__(self, nombres, apellidos, documento, direccion, municipio, ocupacion, parentesco, num1, num2, email, password):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento = documento
        self.direccion = direccion
        self.municipio = municipio
        self.ocupacion = ocupacion
        self.parentesco = parentesco
        self.num1 = num1
        self.num2 = num2
        self.email = email
        self.password = password
    
db.create_all()


class AcudienteSchema(ma.Schema):
    class Meta:
        fields = ('id','nombres', 'apellidos', 'documento', 'direccion', 'municipio', 'ocupacion', 'parentesco', 'num1', 'num2', 'email')


acudiente_schema = AcudienteSchema()
acudientes_schema = AcudienteSchema(many=True)


# ESTE ENPOINT ES PARA CREAR ACUDIENTES
@app.route('/acudientes', methods=['POST'])
def create_acudiente():
    nombres = request.json['nombres']
    apellidos = request.json['apellidos']
    documento = request.json['documento']
    direccion = request.json['direccion']
    municipio = request.json['municipio']
    ocupacion = request.json['ocupacion']
    parentesco = request.json['parentesco']
    num1 = request.json['num1']
    num2 = request.json['num2']
    email = request.json['email']
    password = request.json['password']
    acudiente_task = Acudiente(nombres, apellidos, documento, direccion, municipio, ocupacion, parentesco, num1, num2, email, password)
    db.session.add(acudiente_task)
    db.session.commit()
    return acudiente_schema.jsonify(acudiente_task)


# ESTE ENPOINT ES PARA LISTAR TODOS LOS  ACUDIENTES
@app.route('/acudientes', methods=['GET'])
def get_acudientes():
    all_acudientes = Acudiente.query.all()
    result = acudientes_schema.dump(all_acudientes)
    return jsonify(result)



# ESTE ENPOINT ES PARA OBTENER UN ACUDIENTE POR ID ACUDIENTES
@app.route('/acudientes/<id>', methods=['GET'])
def get_acudiente(id):
    acudiente = Acudiente.query.get(id)
    return acudiente_schema.jsonify(acudiente)


# ESTE ENPOINT ES PARA ACTUALIZAR UN ACUDIENTE POR ID
@app.route('/acudientes/<id>', methods=['PUT'])
def update_acudiente(id):
    acudiente = Acudiente.query.get(id)

    nombres = request.json['nombres']
    apellidos = request.json['apellidos']
    documento = request.json['documento']
    direccion = request.json['direccion']
    municipio = request.json['municipio']
    ocupacion = request.json['ocupacion']
    parentesco = request.json['parentesco']
    num1 = request.json['num1']
    num2 = request.json['num2']
    email = request.json['email']
    password = request.json['password']
    
    acudiente.nombres = nombres
    acudiente.apellidos = apellidos
    acudiente.documento = documento
    acudiente.direccion = direccion
    acudiente.municipio = municipio
    acudiente.ocupacion = ocupacion
    acudiente.parentesco = parentesco
    acudiente.num1 = num1
    acudiente.num2 = num2
    acudiente.email = email
    acudiente.password = password
    db.session.commit()

    return acudiente_schema.jsonify(acudiente)


# ESTE ENPOINT ES PARA BORRAR UN ACUDIENTE POR ID
@app.route('/acudientes/<id>', methods=['DELETE'])
def delete_acudiente(id):
    acudiente = Acudiente.query.get(id)
    db.session.delete(acudiente)
    db.session.commit()
    return acudiente_schema.jsonify(acudiente)





if __name__ == "__main__":
    app.run(debug=True)