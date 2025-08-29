# Infra Practice

This repository contains infrastructure practice exercises using Python and Kubernetes.

## Description
This project includes various Kubernetes manifests for deploying pods, replicas, and deployments. It serves as a hands-on practice for managing containerized applications in a Kubernetes environment.

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/infra_practice.git
    cd infra_practice
    ```

## Project Structure

```
infra_practice/
├── README.md
├── requirements.txt
├── k8/
│   ├── deployment/
│   │   └── deploy.yaml
│   ├── pods/
│   │   ├── labels.yml
│   │   ├── podtest.yml
│   │   └── podtest2.yml
│   └── replicas/
│       └── replica1.yml
└── src/
```

## Usage

- **Kubernetes manifests:**  
  Apply Kubernetes resources from the `k8` directory:
  ```bash
  kubectl apply -f k8/deployment/deploy.yaml
  kubectl apply -f k8/pods/podtest2.yml
  kubectl apply -f k8/replicas/replica1.yml
  ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

This project is licensed under the MIT License.