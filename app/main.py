from fastapi import FastAPI, Depends
from app.dependencies import enforce_rate_limit


app = FastAPI()

@app.get('/health')
def get_health():
    return {'status': 'ok'}

@app.get('/ping', dependencies=[Depends(enforce_rate_limit)])
def ping():
    return {'message': 'pong'}