from flask import Flask #nome minusculo pacote, nome maiusculo recurso/classe
from flask_restful import Api
from resources.hotel import Hoteis, Hotel # pasta que se torna pacote e dentro deste pacote, estamos chamando o arquivo hotel e importando a classe hoteis que é um recurso

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request #antes de tudo verifica se tem banco
def cria_banco(): #criando banco
    banco.create_all() # criando tabela

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__': # se for chamado do app.py vai executar
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

# http://127.0.0.1:5000/hoteis -> raiz do site localhost / hoteis
