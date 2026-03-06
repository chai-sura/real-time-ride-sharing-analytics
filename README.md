# Real-Time Ride Sharing Analytics System

This project implements a real-time analytics pipeline for ride-sharing platforms to process ride events, compute metrics, detect anomalies, and expose insights via an API.

## Architecture

Ride Events → Kafka (AWS MSK) → Kafka Streams Processing → MongoDB Atlas → GraphQL API → Dashboard

## Key Features

- Processes **100K+ ride events/day** using Kafka Streams
- Real-time driver and city ride metrics
- Detects anomalies in ride activity
- Stores aggregated metrics in **MongoDB Atlas**
- Provides insights through **GraphQL API**
- Performance monitoring via **Grafana dashboards**
- Containerized deployment using **Docker + Kubernetes (EKS)**

## Tech Stack

- Python
- Apache Kafka Streams
- AWS MSK
- MongoDB Atlas
- GraphQL
- Docker
- Kubernetes (EKS)
- Grafana

## Example Metrics Generated

- Rides per city
- Average trip distance
- Driver utilization
- Surge activity detection
- Ride demand spikes

## Project Structure

data-generator → simulates ride events  
kafka-streams-app → processes real-time streams  
graphql-api → exposes aggregated metrics  
dashboards → monitoring dashboards  

## How to Run Locally

1. Start Kafka
2. Run ride event producer
3. Run stream processor
4. Start GraphQL API
5. View metrics via API or Grafana
