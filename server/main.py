from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from model import OrderDetails
import db_utils


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to DesiDelights"}

@app.post("/")
async def handle_dialogflow_request(request: Request, session: AsyncSession = Depends(get_db)):
    payload = await request.json()
    print(payload)
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    if intent=="ongoing-tracking.provide_id":
        order_status = await db_utils.get_order_status(parameters["number"], session)
        fulfillment_text = f"Your order is {order_status}" if order_status  else  "Sorry, I couldn't find any details for your order."
        return JSONResponse(content={
            "fulfillmentText": fulfillment_text,
        })


