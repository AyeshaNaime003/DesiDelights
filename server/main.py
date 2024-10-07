from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import db_utils
import utils

ongoing_orders = {}
        
async def ongoing_tracking_provide_id(parameters: dict, session: AsyncSession):
    order_id = int(parameters["number"])
    order_status = await db_utils.get_order_status(order_id, session)
    return f"Order {order_id} is {order_status}" if order_status else "Sorry, couldn't find any details for your order."

async def ongoing_order_add(parameters: dict, session: AsyncSession):
    global ongoing_orders
    menu_items = parameters["menu-items"]
    quantities = parameters["number"]
    
    if len(menu_items)!=len(quantities):
        return "Please specify quanity for each item" 
    else: 
        session_id = parameters["session_id"].split('/')[-1]
        new_menu = dict(zip(menu_items, quantities))
        print(new_menu)
        if session_id in ongoing_orders.keys():
            ongoing_orders[session_id].update(new_menu)
        else:
            ongoing_orders[session_id] = new_menu    
        print(f"\n\n{ongoing_orders}\n\n")
        return f"Order uptil now is {utils.format_order(ongoing_orders[session_id])}. Anything else?"
    
async def ongoing_order_delete(parameters: dict, session: AsyncSession):
    global ongoing_orders
    session_id = parameters["session_id"].split('/')[-1]
    menu_items = list(parameters["menu-items"])
    print(ongoing_orders)
    print(session_id)
    if session_id in ongoing_orders.keys():
        existing_menu = ongoing_orders[session_id]
        for menu_item in menu_items:
            _ = existing_menu.pop(menu_item)
        ongoing_orders[session_id] = ongoing_orders[session_id]
        return f"Order uptil now is {utils.format_order(ongoing_orders[session_id])}. Anything else?"
    else:
        return "Sorry had problem finding your order? Can you please repeat the order"



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
    # print('\n\n'+str(payload)+"\n\n")
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    parameters["session_id"] = payload["session"]

    return JSONResponse(content={"fulfillmentText": await intentHandler[intent](parameters, session)})
       



 