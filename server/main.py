from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from model import OrderDetails
from sqlalchemy.future import select

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to DesiDelights"}

@app.post("/")
async def handle_dialogflow_request(request: Request, session: AsyncSession = Depends(get_db)):
    payload = await request.json()
    # webhookStatus = payload["webhookStatus"]["message"]
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    if intent=="ongoing-tracking.provide_id":
        results = await get_order_details(session, parameters)
        # Let's assume results contain some order details you want to send back
        if results:
            # Building a response in Dialogflow format
            fulfillment_text = f"Here are your order details: {results}"
            return JSONResponse(content={
                "fulfillmentText": fulfillment_text,  # Dialogflow expects 'fulfillmentText' field for response
            })
        else:
            return JSONResponse(content={
                "fulfillmentText": "Sorry, I couldn't find any details for your order.",
            })

    
async def get_order_details(session: AsyncSession, parameters: dict):
    try:
        # Execute the select statement to get all order details
        order_id = parameters.get("number")
        query = select(OrderDetails).where(OrderDetails.order_id == order_id)
        result = await session.execute(query)
        order_details = result.scalars().all()  # Fetch all rows

        return order_details  # This will be a list of OrderDetails instances
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle exceptions as needed

