from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from model import Order, OrderDetails
import db_utils
import utils

ongoing_orders = {}
        
async def ongoing_tracking_provide_id(parameters: dict, session: AsyncSession):
    order_id = int(parameters["number"])
    order_status = await db_utils.get_order_status(order_id, session)
    return (
        f"Order Id {order_id} is currently {order_status}. Thank you for your patience!" 
        if order_status else 
        "I'm sorry, but I couldn't find any details for your order. Please check the ID and try again."
    )


def ongoing_order_add(parameters: dict):
    global ongoing_orders
    menu_items = parameters["menu-items"]
    quantities = parameters["number"]
    
    if len(menu_items)!=len(quantities):
        return "Could you please provide a quantity for each item? Example one plate of Biryani"
    else: 
        session_id = parameters["session_id"].split('/')[-1]
        new_menu = dict(zip(menu_items, quantities))
        print(new_menu)
        if session_id in ongoing_orders.keys():
            ongoing_orders[session_id].update(new_menu)
        else:
            ongoing_orders[session_id] = new_menu    
        print(f"\n\n{ongoing_orders}\n\n")
        return f"Items added Successfully. Order uptil now is {utils.format_order(ongoing_orders[session_id])}. Anything else?"
    

def ongoing_order_delete(parameters: dict):
    global ongoing_orders
    session_id = parameters["session_id"].split('/')[-1]
    menu_items = list(parameters["menu-items"])
    if session_id in ongoing_orders.keys():
        existing_menu = ongoing_orders[session_id]
        items_removed = []
        items_cannot_remove = []
        for menu_item in menu_items:
            if existing_menu.pop(menu_item, None) is None:
                items_cannot_remove.append(menu_item)
            else: 
                items_removed.append(menu_item)
        ongoing_orders[session_id] = existing_menu

        removal_message = ""
        if items_removed:
            removal_message += "Removed: " + ", ".join(items_removed) + ". "
        if items_cannot_remove:
            removal_message += "Unable to remove: " + ", ".join(items_cannot_remove) + ". "
        return_statement = removal_message + f"Your current order is: {utils.format_order(ongoing_orders[session_id])}. Anything else I can help you with?"
        return return_statement
    else:
        return "Sorry had problem finding your order? Can you please repeat the order"


def ongoing_order_delete_all(parameters: dict):
    pass 

def ongoing_order_get_details(parameters: dict):
    pass

async def ongoing_order_finalize(parameters: dict, session: AsyncSession):
    global ongoing_orders
    session_id = parameters["session_id"].split('/')[-1]
    menu = ongoing_orders[session_id]
    if not menu:
        return "No ongoing order found for this session."
    
    # calculate full price and make orders_details rows
    total_bill = 0
    order_details = []
    for item, quantity in menu.items():
        item_id = await db_utils.get_item_id(item, session)
        item_price = await db_utils.get_item_price(item, session)
        
        if item_price is None:
            return f"Sorry, we couldn't find the price for {item}."
        if item_id is None:
            return f"Sorry, we couldn't find the id for {item}."

        item_total_price = item_price * quantity
        total_bill += item_total_price
        order_details.append((item_id, quantity, item_total_price))
    
    # add order
    order_id = await db_utils.save_order(total_bill, session)
    if order_id is None:
        return "We encountered an issue while processing your order. Please try again or contact support."
    
    # Save the order details using the retrieved order ID
    return_code = await db_utils.save_order_details(order_id, order_details, session)
    if return_code is None:
        return "We encountered an issue while processing your order. Please try again or contact support."
    
    formatted_order = utils.format_order(menu)
    ongoing_orders.pop(session_id)
    return (
        f"Your order for {formatted_order} has been successfully placed!\n"
        f"Order ID: {order_id}\n"
        f"Total Bill: PKR{total_bill:.2f}\n"
        "Your order is now being cooked and will be delivered within 20-30 minutes. "
        "Please keep the cash ready for the delivery. Thank you for choosing us!"
    )


intentHandler = {
    "ongoing-tracking.provide_id":ongoing_tracking_provide_id,
    "ongoing-order.add":ongoing_order_add,
    "ongoing-order.delete":ongoing_order_delete,
    "ongoing-order.finalize":ongoing_order_finalize,
    "ongoing_order.delete_all":ongoing_order_delete_all
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

    if intent=="ongoing-tracking.provide_id":
        return JSONResponse(content={"fulfillmentText": await ongoing_tracking_provide_id(parameters, session)})
    elif intent=="ongoing-order.add":
        return JSONResponse(content={"fulfillmentText": ongoing_order_add(parameters)})
    elif intent=="ongoing-order.delete":
        return JSONResponse(content={"fulfillmentText": ongoing_order_delete(parameters)})
    elif intent=="ongoing_order.delete_all":
        return JSONResponse(content={"fulfillmentText": ongoing_order_delete_all(parameters)})
    elif intent=="ongoing-order.finalize":
        return JSONResponse(content={"fulfillmentText": await ongoing_order_finalize(parameters, session)})
