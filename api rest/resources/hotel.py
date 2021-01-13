from flask_restful import Resource, reqparse # reqparse recebe os elementos da requisição
from models.hotel import HotelModel

hoteis = [      # lista de hoteis como lista de dicionarios
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome': 'Gravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
        },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
        }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # objeto transformado em json, cada hotel vai retornar todos elemtnos igual *select * from hoteis

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be blank ")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be blank")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id) #variavel chamada hotel, usando a classe hotel e chamando a função como parametro id_hotel
        if hotel:
            return hotel.json() #se existir retorna o hotel
        return {'message': 'Hotel não existe.'}, 404 # not found , se o hotel não for encontrado mostra isto

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #bad request

        dados = Hotel.atributos.parse_args() #pega os atributos da classe e passa pra variavel
        hotel = HotelModel(hotel_id, **dados) #objeto do tipo hotel kwargs
        try: #tente salvar
            hotel.save_hotel() #salva o hotel no banco de dados
        except: #se nao conseguir, exiba a mensagem
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # internal server error
        return hotel.json() # retornado em json o hotel criado


    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id) #tenta encontrar hotel
        if hotel_encontrado: #se encontrar
            hotel_encontrado.update_hotel(**dados) #atualiza novo hotel
            hotel_encontrado.save_hotel() # objeto atualizado salvo no banco
            return hotel_encontrado.json(), 200 #ok
        hotel = HotelModel(hotel_id, **dados) # instanciar objeto
        try: #tentando salvar
            hotel.save_hotel() #salva o hotel no banco de dados
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # internal server error
        return hotel.json(), 201 #created

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id) #encontrando hotel
        if hotel:
            try:
                hotel.delete_hotel() #deletando hotel
            except:
                return {'message': 'An error ocurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'hotel not found'}, 404
