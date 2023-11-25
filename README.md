# local launch reminders
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
