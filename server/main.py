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
    if intent=="ongoing-tracking.provide_id":
        results = await get_order_details(session)
        print(type(results))
        print(results)
        return {"message":"sucess ongoing-tracking.provide_id"}
    
async def get_order_details(session: AsyncSession):
    try:
        # Execute the select statement to get all order details
        result = await session.execute(select(OrderDetails))
        order_details = result.scalars().all()  # Fetch all rows

        return order_details  # This will be a list of OrderDetails instances
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Handle exceptions as needed

