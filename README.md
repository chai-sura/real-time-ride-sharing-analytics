# Real-Time Ride-Sharing Analytics on AWS

A production-grade, real-time analytics system for ride-sharing events built with **Apache Kafka (AWS MSK)**, **MongoDB Atlas**, **FastAPI/GraphQL**, **Prometheus**, and **Grafana**, deployed on **AWS EKS**.

---

## 🏗️ Architecture Overview
```
flowchart LR
    A[Event Generator] --> B[AWS MSK\nKafka Broker]
    B --> C[Stream Processor\non AWS EKS]
    C --> D[MongoDB Atlas]
    C --> E[GraphQL API\non AWS EKS]
    E --> F[Prometheus\nMetrics]
    F --> G[Grafana\nDashboards]
```
```
┌─────────────────┐
│  Ride Events    │
│  Producer       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Kafka Topic    │  ← AWS MSK
│  ride-events    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Stream         │  ← AWS EKS / Docker
│  Processor      │
│  - Consumes     │
│    Kafka events │
│  - Writes to    │
│    MongoDB      │  ← MongoDB Atlas
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GraphQL API    │  ← FastAPI + Strawberry
│  Exposes Ride   │
│  Metrics        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Prometheus     │
│  + Grafana      │
│  Monitoring     │
└─────────────────┘
```

---

## ✨ Key Features

- **Real-time ingestion** of ride events via Kafka on AWS MSK
- **Stream processing & aggregation** using a Dockerized Python processor on AWS EKS
- **Persistent storage** in MongoDB Atlas for analytics and querying
- **GraphQL API** for city-level and global ride metrics (FastAPI + Strawberry)
- **Observability** with Prometheus metrics and Grafana dashboards
- Designed to handle **100K+ ride events/day** with **sub-200ms processing latency**

---

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.12+
- The following ports available locally:

| Service     | Port |
|-------------|------|
| Kafka       | 9092 |
| Zookeeper   | 2181 |
| MongoDB     | 27017|
| API         | 8000 |
| Prometheus  | 9090 |
| Grafana     | 3000 |

---

## 🚀 Getting Started

Clone the repository and start all services with Docker Compose:
```bash
git clone https://github.com/chai-sura/real-time-ride-sharing-analytics.git
cd real-time-ride-sharing-analytics
docker-compose up -d
```

---

## 📁 Project Structure
```
real-time-ride-sharing-analytics/
├── data_generator/          # Kafka producer — generates synthetic ride events
├── stream_processor/        # Kafka consumer — processes and writes to MongoDB
├── graphql_api/             # FastAPI + Strawberry GraphQL server
├── dashboards/              # Grafana dashboard JSON configs
├── monitoring/              # Prometheus configuration
├── Dockerfiles/             # Per-service Dockerfiles
├── docker-compose.yml       # Local orchestration
└── requirements.txt         # Python dependencies
```

---

## 📊 Monitoring

Once running, access the dashboards at:

- **Grafana**: [http://localhost:3000](http://localhost:3000)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **GraphQL Playground**: [http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 🛠️ Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Event Stream  | Apache Kafka (AWS MSK)            |
| Processing    | Python, Docker, AWS EKS           |
| Storage       | MongoDB Atlas                     |
| API           | FastAPI, Strawberry (GraphQL)     |
| Monitoring    | Prometheus, Grafana               |
| Infrastructure| AWS (MSK, EKS)                   |
