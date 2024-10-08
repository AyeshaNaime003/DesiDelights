from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from model import MenuItem, Order, OrderDetails

def format_order_details_and_status(details, status):
    pass

async def get_order_details(order_id, session: AsyncSession):
    query = (
        select(MenuItem.name, OrderDetails.quantity, OrderDetails.total_price)
        .join(MenuItem, OrderDetails.item_id == MenuItem.item_id)  # Joining on item_id
        .where(OrderDetails.order_id == order_id)  # Filtering by order_id
    )
    result = await session.execute(query)
    order_details = result.all()  # Fetch all results
    return [
        {"order_id": detail[0], "name": detail[0], "quantity": detail[1], "total_price": detail[2]}
        for detail in order_details
    ]


async def get_order_status(order_id, session: AsyncSession):
    try:
        # Create the query and execute
        query = select(Order.status).where(Order.order_id == order_id)
        result = await session.execute(query)
        order_status = result.scalar_one_or_none()
        return order_status
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 

async def get_item_id(item_name: str, session: AsyncSession):
    try:
        query = text("SELECT get_id_for_item(:item_name)") 
        result = await session.execute(query, {"item_name": item_name}) 
        id = result.scalar_one_or_none()  # id will be None if no result found
        if id==-1:
            return None
        else:
            return int(id) 
    except Exception as e:
        print(f"An error occurred while getting item id: {e}")
        await session.rollback()
        return None

async def get_item_price(item_name: str, session: AsyncSession):
    try:
        query = text("SELECT get_price_for_item(:item_name)") 
        result = await session.execute(query, {"item_name": item_name}) 
        price = result.scalar_one_or_none() # price will be None if no result found
        if price==-1:
            return None
        else:
            return int(price) 
    except Exception as e:
        print(f"An error occurred while getting item price: {e}")
        await session.rollback()
        return None

async def save_order(total_bill: float, session: AsyncSession):
    try:
        new_order = Order(bill=total_bill, status="cooking")
        session.add(new_order)
        await session.commit()
        return new_order.order_id
    except Exception as e:
        print(f"An error occurred while saving the order: {e}")
        return None
    
# Function to save the order details using the order ID
async def save_order_details(order_id: int, order_details: list, session: AsyncSession):
    try:
        for item_id, quantity, item_total_price in order_details:
            new_order_detail = OrderDetails(order_id=order_id, item_id=item_id, quantity=quantity, total_price=item_total_price)
            session.add(new_order_detail)
        await session.commit()
        return 200
    except Exception as e:
        print(f"An error occurred while saving order details: {e}")
        return None