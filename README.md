## UAV Monitoring Platform

### Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Getting Started

1. Clone the repository:
```bash
git clone git@github.com:alikamilyagli/uav-monitoring-platform.git
cd uav-monitoring-platform
```

2. Run the following command to start the application:
```bash
docker-compose up --build
```

3. Access the frontend and backend applications in your browser:
- Frontend UI: http://localhost:8080
- Backend API: http://localhost:5001
- Minio UI: http://localhost:9001/login
- Minio Username: `miniouser`
- Minio Password: `miniopw123`


4. To stop the application, use `Ctrl + C`, and then run:
```bash
docker-compose down
```


