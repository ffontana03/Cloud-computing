# Resilient and Secure Microservices Architecture based on Apache Kafka

This repository contains the practical implementation of a Cloud-Native distributed messaging system based on Apache Kafka. The project was developed as a university Proof of Concept (PoC) to demonstrate advanced Non-Functional Requirements (NFRs) such as **High Availability (HA)**, **Fault Tolerance**, and **Cybersecurity (SASL/SSL)**.

---

## 📌 Project Overview

The architecture simulates an E-commerce environment with two decoupled Python microservices:

- **Producer (`producer.py`)**: Simulates the rapid ingestion of user orders.
- **Consumer (`consumer.py`)**: Acts as a billing group, processing the orders asynchronously.

The Kafka cluster is composed of **3 Broker Nodes** running on Docker Compose, utilizing the **KRaft** consensus protocol (ZooKeeper-less) to ensure High Availability and Zero Data Loss through strict replication policies (`Replication Factor = 3`, `acks=all`).

---

## ⚙️ Prerequisites

To run this project locally, you need:

- [Docker](https://www.docker.com/) and Docker Compose
- [Python 3.8+](https://www.python.org/)
- [OpenSSL](https://www.openssl.org/) (for local certificate generation)

---

## 🔒 Security Setup (IMPORTANT)

Following strict Cybersecurity and *Infrastructure as Code (IaC)* best practices, the private keys and keystores (`.key` and `.p12` files) have been intentionally excluded from this repository via `.gitignore`.

**Before starting the cluster, you must generate the local self-signed certificates.** Open a terminal in the project root and run the following OpenSSL commands:

**1. Generate the Private Key and Public Certificate:**
```bash
openssl req -newkey rsa:2048 -nodes -keyout broker.key -x509 -days 365 -out broker.crt -subj "//CN=localhost"
```

**2. Package them into a PKCS12 Keystore:**
```bash
openssl pkcs12 -export -in broker.crt -inkey broker.key -out kafka.keystore.p12 -name kafka -passout pass:PasswordSicura123!
```

> **Note:** The password must be exactly `PasswordSicura123!` to match the Docker Compose configuration.

---

## 🚀 How to Run the Environment

### 1. Start the Kafka Cluster

Run the following command to provision the 3 brokers and the UI container:
```bash
docker compose up -d
```

You can monitor the cluster health and topology by accessing the Kafka UI at: `http://localhost:8080`

### 2. Run the Microservices

Install the required Python dependencies:
```bash
pip install confluent-kafka
```

Open two separate terminals and run the clients:

- **Terminal 1 (Consumer):** `python consumer.py`
- **Terminal 2 (Producer):** `python producer.py`

---

## 🧪 Testing the Architecture

### Fault Tolerance Test (Disaster Recovery)

While the Python scripts are running, simulate a broker crash by stopping one of the nodes:
```bash
docker stop kafka-1
```

> **Expected Result:** The cluster will lose a node (visible as Under Replicated Partitions in the UI), but the Python Producer and Consumer will continue to process messages without any data loss or downtime, proving the system's resilience.

### Security Test (Authentication Failure)

Edit the `producer.py` or `consumer.py` file and change the `sasl.password` to an incorrect value (e.g., `Hacker123`). Restart the script.

> **Expected Result:** The connection will be immediately rejected by the brokers with an `Authentication failed` error, proving the effectiveness of the SASL/PLAIN JAAS layer.

---

## 👤 Author

**Federico Fontana** (Mat. 81058A)
