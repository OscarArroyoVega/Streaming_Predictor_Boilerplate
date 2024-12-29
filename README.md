# Real-Time ML Trading System

This repository contains a collection of microservices developed during the "Building Real-Time ML Systems" cohort (3rd version), guided by Pau Labarta Bajo. The system processes real-time trading data and predicts variations in trading pairs using data from various APIs.

## Overview

The system is designed to capture, process, and analyze trading data in real-time, utilizing modern data engineering and ML practices through a microservices architecture.

## Tech Stack

### Package Management & Build Tools
- **Poetry**: Modern dependency management and packaging tool that simplifies dependency resolution and package building
- **uv**: Ultra-fast Python package installer and resolver, offering significant performance improvements over pip
- **Make**: Automation tool used for streamlining build processes and command execution

### Data Processing & Validation
- **Pydantic**: Data validation using Python type annotations, ensuring type safety and automatic validation of data structures
- **Pydantic Settings**: Environment variables and configuration management with automatic type parsing and validation
- **Quixstreams**: Real-time data processing framework optimized for streaming applications
- **Redpanda**: A modern streaming platform compatible with Kafka protocols, offering improved performance and simpler operations

### Development Tools
- **Ruff**: Ultra-fast Python linter and code formatter, helping maintain consistent code style and catch potential issues
- **Docker**: Containerization platform ensuring consistent environments across development and production

## System Architecture

The system consists of several microservices:
- Trade data ingestion service
- Data processing and feature engineering service
- ML prediction service
- API service for external communication

Each service is containerized and communicates through Redpanda/Kafka message queues, ensuring scalability and reliability.

## Features

- Real-time data ingestion from various trading APIs
- Stream processing of trading data
- ML-based prediction of trading pair variations
- Scalable microservices architecture
- Containerized deployment

## Acknowledgments

This project was developed as part of the "Building Real-Time ML Systems" cohort led by Pau Labarta Bajo. Special thanks to all cohort participants for their insights and contributions.
