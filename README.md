 how the FastAPI endpoints work, the structure of the database (maybe with an ER diagram), and more about how the chatbot interacts with the API.
# Desi Delights - Online Chatbot Resturant with FastAPI and PostgreSQL Database
## Summary
This project is a full-stack restaurant chatbot solution built using FastAPI, PostgreSQL, and Google's DialogFlow. The chatbot allows customers to browse the menu, place and track orders, and finalize payments. The backend is powered by FastAPI for API communication, while DialogFlow handles natural language processing for smooth user interactions. All order and menu data is managed via a PostgreSQL database. Ngrok is used to secure communication between the API and chatbot.

## Features
## Components
### 1. PostgreSQL Database:
install postgresql and pgadmin
make database called `desi_delights`
rigth click on it, open query tool, copy and paste code from `db/desi_delight.sql` into the query tool and Run it
You should get output like this 
``` 
NOTICE:  table "menu_items" does not exist, skipping
NOTICE:  table "orders" does not exist, skipping
NOTICE:  table "orders_details" does not exist, skipping
NOTICE:  function get_price_for_item() does not exist, skipping
CREATE FUNCTION

Query returned successfully in 101 msec.
``` 
__Note: feel free to change the menu items or anything else you want__

### 2. FASTAPI:


### 3. Google's DialogFlow:
    Make context for each feature, context is basically how many user-chatbot dialogues contribute to the gettign the feature done
    add intents to context:
    1. ongoing-order: making a new order for the user, adding and removing items, once finalized, dump the order to database
        a. ongoing-order.new
        b. ongoing-order.add
        c. ongoing-order.remove
        d. ongoing-order.finalize
    2. ongoing-tracking: Tracking the users order 

    also explain the standards being used 

Dialog flow fulfillement allow dialogflow to send the input's analysis to our fastapi app, but for this  our fastapi's host should be secure
Use ngrok

### 4. Ngrok:
Ngrok: 
download for your pc, extract and copy ngrok.exe to server dircetory
make account and get authentication token, and save it in ngrok.yml in server directory
```yml
authtoken: your_token_here
```
and secure your http port using
``` cmd
ngrok http 8000 --config=./ngrok.yml
```