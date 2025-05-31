# humble-bee
An iterative project to deploy a web app with GitHub Actions, and ArgoCD for the K8s env

# System schema
![image](https://github.com/user-attachments/assets/15c3c71c-cd99-443b-8a94-1cf9bc498d0a)

# K3s node
Debian VM with an instance of k3s
```
curl -sfL https://get.k3s.io | sh - 
```

# Why ArgoCD
- Being pulled base, using ArgoCD would not require the access key to the on-prem VM to be stored in public.
- The sync of the new config yaml will be done periodically



# Setting up ArgoCD on VM
```
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```

argocd-app.yaml
``` argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: python-webapp
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

## Configure Ingress for ArgoCD
```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "ClusterIP"}}'
```

## Force update
```
kubectl annotate application python-webapp   -n argocd argocd.argoproj.io/refresh=hard --overwrite
```

## Get ArgoCD credentials:
```
user: admin
pass: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

# Configuring monitoring for k3s pods and services on the VM
## Prometheus + Grafana
Installation using Helm Chart