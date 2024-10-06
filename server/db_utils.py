from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model import MenuItem, Order, OrderDetails

def format_order_details_and_status(details, status):
    pass

async def get_order_details(order_id, session: AsyncSession):
    try:
        # Create the query and execute
        query = select(OrderDetails).where(OrderDetails.order_id == order_id)
        result = await session.execute(query)
        order_details = result.scalars().all()  
        return order_details  
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  

async def get_order_status(order_id, session: AsyncSession):
    try:
        # Create the query and execute
        query = select(Order.status).where(Order.order_id == order_id)
        result = await session.execute(query)
        order_status = result.scalars().first()
        if order_status is not None:
            return str(order_status)  # Directly return the order status
        else:
            return None  # Handle case where order_id does not exist
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  
