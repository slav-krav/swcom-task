# k8s launch
1. Build an image from app's root folder.
```shell
docker build --tag=userapp .
```
2. Run local k8s cluster with minikube and upload just built image there.
```shell
minikube start
minikube image load usersapp:latest
```
3. Confirm that image is uploaded
```shell
minikube image ls --format table

|-----------------------------------------|---------|---------------|--------|
|                  Image                  |   Tag   |   Image ID    |  Size  |
|-----------------------------------------|---------|---------------|--------|
|                                     ...                                    |
| docker.io/library/usersapp              | latest  | 75c50e6e5a465 | 1.09GB |
|                                     ...                                    |
|-----------------------------------------|---------|---------------|--------|
```
4. Apply k8s manifests to your minikube cluster with
```shell
kubectl apply -f "path_to_repo/deploy"
```
5. Expose your service with minikube tool
```shell
minikube service users-app-service --url
```
Get printed IP address, copy it and paste to your browser
6. ..

# Known issues
Due to time my personal limits and task description I had to omit usage of some best practises. 
Thus, some unfortunate flaws present, here are some of them: 
1. Py app far from ideal app: 
   - No tests 
   - Service is stateful (sqllite data is in container with the py service). 
   - Py app is not fully user-friendly. For example, if you will try to create two users with same email,
which violates DB constraint, you will get `Internal server error` instead of user-friendly error
   
2. No real authentication. Only authorisation. JWT token will be generated at the moment of user creation.
3. JWT salt is hardcoded to `SECRET` value.
4. Usage of `latest` docker tag



# Local non-containerized launch reminders
1. Run fast api server
```shell
cd api
uvicorn main:app --reload
```
2. Run opa server locally: 
```shell
cd opa
opa run -s --addr localhost:8181 -b .
```


