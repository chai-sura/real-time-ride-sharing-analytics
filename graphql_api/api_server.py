# api_server.py
import threading
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from pymongo import MongoClient
from prometheus_client import Counter, Histogram, make_wsgi_app
from wsgiref.simple_server import make_server

# -------------------------
# MongoDB connection
# -------------------------
client = MongoClient("mongodb://mongo:27017/")  # use service name 'mongo' in docker
db = client["ride_analytics"]

# -------------------------
# Prometheus metrics
# -------------------------
REQUEST_COUNT = Counter("api_request_count", "Total number of API requests")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latency of API requests in seconds")

# Create Prometheus WSGI app
app_prometheus = make_wsgi_app()

def start_prometheus_server():
    # Bind to 0.0.0.0 so other containers (Prometheus) can access it
    server = make_server('0.0.0.0', 8001, app_prometheus)
    server.serve_forever()

# Start Prometheus server in a separate thread
threading.Thread(target=start_prometheus_server, daemon=True).start()

# -------------------------
# GraphQL types
# -------------------------
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

# -------------------------
# GraphQL Query
# -------------------------
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
                )
                for d in data
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

# -------------------------
# FastAPI + GraphQL setup
# -------------------------
schema = strawberry.Schema(query=Query)
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Real-time Ride Sharing Analytics API running!"}