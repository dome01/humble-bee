# humble-bee
An iterative project to deploy a web app with GitHub Actions, and ArgoCD for the K8s env

# System schema
![image](https://github.com/user-attachments/assets/28eef135-c138-41e9-8314-8f2e35d4fa04)


# K3s node
Debian VM with an instance of k3s
```
curl -sfL https://get.k3s.io | sh - 
```

# Why ArgoCD
- Being pulled base, using ArgoCD would not require the access key to the on-prem VM to be stored in public.
- The sync of the new config yaml will be done periodically
