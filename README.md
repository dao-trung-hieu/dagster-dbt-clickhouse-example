# Dagster, dbt, and ClickHouse Example

This repository demonstrates how to integrate **Dagster**, **dbt**, and **ClickHouse** to create a data pipeline for extracting, transforming, and loading (ETL) data efficiently.

## 🚀 Overview

- **Dagster**: Orchestrates the data pipeline, schedules jobs, and provides monitoring.
- **dbt (Data Build Tool)**: Handles SQL-based transformations, making data modeling easier.
- **ClickHouse**: A fast columnar database optimized for analytical workloads.

This project uses **Docker Compose** to spin up a local environment with all necessary components.

---

## 📂 Project Structure
```bash
dagster-dbt-clickhouse-example/
│── dags/                     # Dagster pipeline definitions
│── dbt_project/               # dbt models and transformations
│── clickhouse/                # ClickHouse setup
│── docker-compose.yaml        # Docker Compose configuration
│── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```
---

## 🛠️ Setup and Installation

### 1️⃣ Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose**: [Get Docker](https://docs.docker.com/get-docker/)
- **Git**: [Install Git](https://git-scm.com/)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/dao-trung-hieu/dagster-dbt-clickhouse-example.git
cd dagster-dbt-clickhouse-example
```

### 3️⃣ Start the Services

```bash
sudo docker compose up --build
```
This will spin up:

	•	Dagster
	•	dbt
	•	ClickHouse

4️⃣ Access the Dagster UI

Once the services are running, open your browser and go to:

	•	Dagster UI: http://localhost:3000

