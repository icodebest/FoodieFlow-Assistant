from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper

app = FastAPI()

@app.post("/")  
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload.get("queryResult", {}).get("intent", {}).get("displayName", "")
    parameters = payload.get("queryResult", {}).get("parameters", {})


    intent_handler_dict={
        'order.add-context: ongoing-order': add_to_order,
        # 'order.remove-context: ongoing-order':remove_from_order,
        # 'order.complete-context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order,
    }

    return  intent_handler_dict[intent](parameters)


def add_to_order(parameters: dict):
    food_items=parameters["food_items"]
    quantities=parameters["number"]

def track_order(parameters: dict):
    order_id = parameters.get("order_id")

    try:
        order_id = int(order_id)
    except (TypeError, ValueError):
        return JSONResponse(
            content={"fulfillmentText": "That Order ID looks invalid. Please send a numeric ID."}
        )

    status = db_helper.get_order_status(order_id)

    if status:
        response_text = f"Your order with ID {order_id} is currently *{status}*."
    else:
        response_text = f"Sorry, I couldn't find any order with ID {order_id}."

    return JSONResponse(content={"fulfillmentText": response_text})
