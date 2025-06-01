# humble-bee
An iterative microservice project demonstrating GitHub Actions CI/CD with ArgoCD in a K3s Kubernetes environment. The repo evolves from a minimal ID generator service into a basic Twitter-style backend.

# Stack
- **FastAPI** (REST microservices)
- **Supabase (PostgreSQL)** for storage
- **K3s** (lightweight Kubernetes)
- **ArgoCD** for GitOps-based deployment
- **GitHub Actions** for CI/CD
- **Traefik Ingress** for routing
# System schema
![image](https://github.com/user-attachments/assets/15c3c71c-cd99-443b-8a94-1cf9bc498d0a)

# Phase 1 – IDGen Service

A minimal FastAPI service used to:
- Generate UUIDs
- Validate the GitHub Actions pipeline
- Set up ArgoCD sync
- Test Docker image build, deployment, ingress routing, and metrics

```
POST /ids
```
This acted as a “hello world” for infrastructure.

# Phase 2 – Twitter-Style Backend (MVP)
All services follow a consistent REST design with /api/v1/ prefixes and share a single Supabase database.

1. **user-api**
- Create user
```
POST /api/v1/users
```
- Query Params:
  - username (string) : unique identifier for the user
- Follow another user
```
POST /api/v1/follow
```
- Query Params:
  - follower_username (string)
  - followed_username (string)
2. **post-api**
- Post a tweet-like message
```
POST /api/v1/posts
```
- Query Params:
  - username (string)
  - content (string)
3. **feed-api**
- Fetch recent posts from followed users
```
GET /api/v1/feed
```
- Query Params:
  - username (string) : the user whose feed is requested


## Database Schema (Supabase)
```sql
create table users (
  username text primary key
);

create table follows (
  follower_username text references users(username),
  followed_username text references users(username),
  primary key (follower_username, followed_username)
);

create table posts (
  username text references users(username),
  content text,
  created_at timestamp default now()
);
```


## CI/CD with GitHub Actions + ArgoCD

**GitHub Actions**
- Runs tests using pytest
- Builds and pushes Docker images to GHCR
- Deploys K8s manifests via ArgoCD sync

**ArgoCD**
- Monitors this repo (k8s/) and auto-syncs on changes
- Fully declarative GitOps
- Being pulled base, using ArgoCD would not require the access key to the on-prem VM to be stored in public.
- ArgoCD server is exposed using ingress to be accessed from the localhost

<img width="1546" alt="image" src="https://github.com/user-attachments/assets/39b187ee-10bc-41e1-a7ba-7a6ba3057709" />


## Secrets Management

Secrets are passed through GitHub Actions for build context (SUPABASE_URL, SUPABASE_KEY)


# Setup and Troubleshooting
## Install K3s (Kubernetes Lightweight)
The project uses k3s on a Debian VM, installed with the following command:
```
curl -sfL https://get.k3s.io | sh - 
```

## Setting up ArgoCD on VM
Create the namespace and deploy ArgoCD:
```
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```
### Bootstrap the ArgoCD Application
ArgoCD needs to know what application to track and where our repo is. This is done via a manifest like argocd-app.yaml.
```yaml
# k8s/argocd/argocd-app.yaml

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: humble-bee
  namespace: argocd
spec:
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  source:
    repoURL: https://github.com/dome01/humble-bee
    targetRevision: HEAD
    path: k8s
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

### Get ArgoCD admin credential:
```
# Username
admin

# Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Demo & Usage Examples
<img width="1264" alt="image" src="https://github.com/user-attachments/assets/77aa282d-c7e3-4385-9cbf-1b65dc51b9c7" />

### Domain Setup for Local Development
To make Ingress routing work with custom domains like idgen.local or twitter.local, we need to update /etc/hosts file on host machine to map these domains to the IP address of the K3s VM:
```
<IP-of-the-VM>   argocd.local
<IP-of-the-VM>   idgen.local
<IP-of-the-VM>   twitter.local
```
This setup allows access to services like:
- ArgoCD UI: https://argocd.local
- ID generator API: https://idgen.local
- Twitter API suite: https://twitter.local/api/v1/... 

# Next Steps
- Monitoring with Prometheus/Grafana
