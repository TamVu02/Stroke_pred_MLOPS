# Stroke Prediction Model Deployment
    **Table of contents**
        Introduction
        Repository’s structure
        Prerequisites installation
        Deploy Docker services
        Deploy K8S services

## Introduction
This is an educational project focused on how to design and implement a MLOPs workflow. This repo provides a comprehensive guide on building and deploying machine learning models through a complete pipeline, incorporating CI/CD practices and resource management, when also demonstrates the practical application of MLOps solutions to address real-world challenges in deploying AI/ML systems at scale.
- Source code versioning and control: Git/Github
- Containerization: Docker
- Manage and orchestrate containerized applications: K8S, Helm
- Model registry: MLFlow
- Model serving: FastAPI
- CI/CD: Jenkins
- Model span tracing: Jaeger Tracing
- Metrics collector: Prometheus,Cadvisor
- Metrics visualization: Grafana
- Logs collector: ElasticSearch, Kibana


## Repository’s structure
```shell
Stroke_pred_MLOPS/
    ├── dataset/                         # **Data directory**
    │   ├── raw_data/                    # Raw input data
    │   └── processed_data/              # Cleaned and processed data
    │
    ├── src/                             # **Source code**
    │   ├── notebook/                    # Jupyter notebooks for EDA and experiments
    │   ├── test_src/                    # Pytest code
    │   └── train_src/                   # Training pipeline scripts (Log model to Mlflow)
    │   ├── deploy.sh                    # Shell script for deployment Model serving API
    │   ├── JenkinsFile                  # CI/CD pipeline using Jenkins
    │
    ├── model/                           # **Trained model files**
    │   └── stroke_pred_model.joblib     # Serialized model object
    │
    ├── service/                         # **MLOps infrastructure services deployment using Docker**
    │   ├── alertmanager/                # Alertmanager configs
    │   ├── elk/                         # ELK stack for logging
    │   └──└── elk-docker-compose.yml    # Docker Compose for ELK services
    │   ├── grafana/                     # Grafana dashboards
    │   ├── jenkins/                     # Jenkins pipelines/config
    │   └──└── docker-compose.yml        # Docker Compose for Jenkins service
    │   ├── mlflow/                      # MLflow tracking setup
    │   │   └──└── docker-compose.yml    # Docker Compose for Mlflow service
    │   ├── model_api_serving/           # FastAPI or Flask model serving code
    │   │   └──└── docker-compose.yml    # Docker Compose for FastAPI model serving service
    │   └── prometheus/                  # Prometheus monitoring setup
    │   ├── prom-graf-jaeger-docker-compose.yaml  # Docker Compose for services (Prometheus, Grafana, Jaeger)
    │   ├── README.md                    # Guide for set up services on Docker 
    │
    ├── k8s/                             # **Helm chart to deploy services to K8S**
    │   ├── grafana_chart/               # Helm chart for Grafana
    │   ├── prometheus_chart/            # Helm chart for Prometheus
    │   └── stroke-api-chart/            # Helm chart for the stroke prediction API
    │   ├── README.md                    # Guide for set up services on K8S
    │
    ├── references/images                # References images
    │
    ├── requirements.txt                 # Python dependencies
    └── README.md                        # Project overview and documentation
```
                                        


