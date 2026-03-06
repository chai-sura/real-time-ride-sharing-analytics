# api_server.py
import threading
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from pymongo import MongoClient
from prometheus_client import start_http_server, Counter, Histogram

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ride_analytics"]

# Prometheus metrics
REQUEST_COUNT = Counter("api_request_count", "Total number of API requests")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latency of API requests in seconds")

# Start Prometheus metrics server on port 8001
threading.Thread(target=start_http_server, args=(8001,), daemon=True).start()

# GraphQL types
@strawberry.type
class CityMetrics:
    city: str
    rides: int
    revenue: float

@strawberry.type
class RideStats:
    total_rides: int
    total_revenue: float
    cities: list[CityMetrics]

# GraphQL Query
@strawberry.type
class Query:

    @strawberry.field
    def city_metrics(self) -> list[CityMetrics]:
        REQUEST_COUNT.inc()
        with REQUEST_LATENCY.time():
            data = db.city_metrics.find()
            return [
                CityMetrics(
                    city=d["city"],
                    rides=d["rides"],
                    revenue=d["revenue"]
                ) for d in data
            ]

    @strawberry.field
    def ride_stats(self) -> RideStats:
        REQUEST_COUNT.inc()
        with REQUEST_LATENCY.time():
            data = list(db.city_metrics.find())
            total_rides = sum(d["rides"] for d in data)
            total_revenue = sum(d["revenue"] for d in data)
            cities = [
                CityMetrics(city=d["city"], rides=d["rides"], revenue=d["revenue"])
                for d in data
            ]
            return RideStats(total_rides=total_rides, total_revenue=total_revenue, cities=cities)

# Create GraphQL schema
schema = strawberry.Schema(query=Query)

# Create FastAPI app
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Real-time Ride Sharing Analytics API running!"}
