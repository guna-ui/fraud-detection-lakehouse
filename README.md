# 🛡️ Sentinel: Multi-Source Fraud Detection Data Pipeline

An end-to-end, production-grade data engineering pipeline designed to detect financial anomalies (velocity spikes, impossible travel, and multi-currency smurfing) across streaming transactions, relational banking data, and external threat feeds.

### 🏗️ Architecture & Core Components (Phase 1)
- **Source 1 (Simulator):** Memory-efficient generator streaming nested JSON swipes with injected anomalies and schema chaos.
- **Source 2 (CRM / Core Banking):** PostgreSQL relational store tracking user demographics, credit limits, and risk profiles.
- **Source 3 (Threat Feeds & FX):** Resilient REST API client (with exponential backoff) and blacklist CSV parser.
- **Data Quality & DLQ:** Pydantic v2 contract enforcement and Dead Letter Queue isolation for malformed events.
- **Storage Layer:** Date-partitioned Snappy Parquet (Bronze Lake) + PostgreSQL analytical warehouse.
- **Transformation & Modeling:** Medallion architecture (Bronze → Silver → Gold) and Kimball Star Schema via dbt Core.
