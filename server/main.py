from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to DesiDelights"}

@app.post("/")
async def handle_dialogflow_request(request: Request):
    payload = await request.json()
    # webhookStatus = payload["webhookStatus"]["message"]
    intent = payload["queryResult"]["intent"]["displayName"]
    if intent=="ongoing-tracking.provide_id":
        return JSONResponse(content={"intent":intent})
    
def get_order_details(parameters: dict):
    pass

