# Real-Time Ride-Sharing Analytics on AWS

A real-time analytics system for ride-sharing events built with **Kafka (MSK)**, **MongoDB Atlas**, **FastAPI/GraphQL**, **Prometheus**, and **Grafana**, deployed on **AWS**.

---

## 🚀 Features

- **Real-time event streaming** via AWS MSK.
- **Kafka Streams processing**: Consume events, aggregate metrics, and store in MongoDB Atlas.
- **GraphQL API**: Query city-level ride metrics and total ride statistics.
- **Monitoring & Observability**: Track API request counts and latency with Prometheus and Grafana.
- **Cloud-Ready Architecture**: Handles 100K+ ride events/day with <200ms latency.

---

## 🏗 AWS Architecture

```mermaid
flowchart LR
    A[Event Generator] --> B[AWS MSK Kafka Broker]
    B --> C[Processor Service on AWS EKS]
    C --> D[MongoDB Atlas]
    C --> E[GraphQL API on AWS EKS]
    E --> F[Prometheus Metrics]
    F --> G[Grafana Dashboards]
