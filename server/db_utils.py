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
        order_status = result.scalars().one_or_none()
        return str(order_status) if order_status else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 
    
def get_menu_items(session: AsyncSession):
    pass
