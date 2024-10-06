from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from model import OrderDetails
import db_utils

ongoing_orders = {}

def format_order(order_dictionary):
    formatted_order = []
    for i, q in order_dictionary.items():
        formatted_order.append(f"{int(q)} {i}")
    formatted_order = ', '.join(formatted_order)
    return formatted_order
        

async def ongoing_tracking_provide_id(parameters: dict, session: AsyncSession):
    order_id = int(parameters["number"])
    order_status = await db_utils.get_order_status(order_id, session)
    return f"Order {order_id} is {order_status}" if order_status else "Sorry, couldn't find any details for your order."

async def ongoing_order_add(parameters: dict, session: AsyncSession):
    menu_items = parameters["menu-items"]
    quantities = parameters["number"]
    
    if len(menu_items)!=len(quantities):
        return "Please specify quanity for each item" 
    else: 
        session_id = parameters["session_id"].split('/')[-1]
        current_session_order = ongoing_orders.get(session_id, {})
        if len(current_session_order)==0:
            print('new session id ')
        else:
            print('existing session id, adding new items')
        for quantity,menu_item in zip(quantities, menu_items):
            current_session_order[menu_item] = quantity
        ongoing_orders[session_id] = current_session_order  
        print('\n\n'+str(ongoing_orders)+'\n\n')
        return f"Order uptil now is {format_order(current_session_order)}. Anything else?"
    
async def ongoing_order_delete():
    pass
async def ongoing_order_finalize():
    pass

intentHandler = {
    "ongoing-tracking.provide_id":ongoing_tracking_provide_id,
    "ongoing-order.add":ongoing_order_add,
    "ongoing-order.delete":ongoing_order_delete,
    "ongoing-order.finalize":ongoing_order_finalize,
}

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to DesiDelights"}

@app.post("/")
async def handle_dialogflow_request(request: Request, session: AsyncSession = Depends(get_db)):
    payload = await request.json()
    print('\n\n'+str(payload)+"\n\n")
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    parameters["session_id"] = payload["session"]

    return JSONResponse(content={"fulfillmentText": await intentHandler[intent](parameters, session)})
       



 