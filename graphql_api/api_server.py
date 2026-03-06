import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ride_analytics"]

@strawberry.type
class CityMetrics:
    city: str
    rides: int
    revenue: float

@strawberry.type
class Query:

    @strawberry.field
    def city_metrics(self) -> list[CityMetrics]:
        data = db.city_metrics.find()
        return [
            CityMetrics(
                city=d["city"],
                rides=d["rides"],
                revenue=d["revenue"]
            ) for d in data
        ]

schema = strawberry.Schema(query=Query)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")