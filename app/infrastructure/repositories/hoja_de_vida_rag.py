from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.domain.entities.hoja_de_vida import HojaDeVida
from app.domain.repositories.hoja_de_vida_rag import HojaDeVidaRepository
from app.infrastructure.schemas.hoja_de_vida_entity import HojaDeVidaEntityRag

# MongoDB connection URL
# MONGO_URL = ("mongodb+srv://entrevistador:swJTdyxG8pJczD0m@clusterentrevistadoria.rtuhiw6.mongodb.net/?retryWrites=true"
#             "&w=majority&appName=ClusterEntrevistadorIA")
# client = AsyncIOMotorClient(MONGO_URL)
# database = client["analizador_hoja_vida_rag"]
# collection = database["hoja_vida"]


class HojaDeVidaMongoRepository(HojaDeVidaRepository):
    def __init__(self, mongo_url):
        self.mongo_url = mongo_url

    async def get_database(self):
        client = AsyncIOMotorClient(self.mongo_url)
        return client["analizador_hoja_vida_rag"]

    async def add(self, hoja_de_vida: HojaDeVida) -> str:
        db = await self.get_database()
        collection = db["hoja_vida"]
        proceso_entrevista = HojaDeVidaEntityRag(
            username=hoja_de_vida.username,
            hoja_de_vida_vect=hoja_de_vida.hoja_de_vida_vect
        )
        result = await collection.insert_one(proceso_entrevista.dict())
        return str(result.inserted_id)

    async def obtener_por_id(self, id_hoja_de_vida: str) -> HojaDeVida:
        db = await self.get_database()
        collection = db["hoja_vida"]
        try:
            data = await collection.find_one({'_id': ObjectId(id_hoja_de_vida)})
            if data:
                return HojaDeVida(
                    username=data.get('username'),
                    hoja_de_vida_vect=data.get('hoja_de_vida_vect')
                )
            else:
                raise Exception(f'HojaDeVida with id {id_hoja_de_vida} not found')
        except Exception as e:
            print(f"An error occurred: {e}")
            return None



