from flask import Flask, request
from pymongo import MongoClient
import yaml
from publisher import publisher
from saga_transaction_logger import write_transaction

app = Flask(__name__)

config = dict()

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

app.config['DEBUG'] = config['debug']
app.config['TESTING'] = config['testing']


@app.route('/booking', methods=['POST'])
def create_booking():
    with MongoClient(config['mongodb']['dsn']) as client:
        db = client['bookings']
        collection = db['bookings']

        payload = {"customer_id": request.json.get("customer_id"),
                   "booking_type": request.json.get("booking_type"),
                   "booking_date": request.json.get("booking_date")}

        result = collection.insert_one(payload)

        payload['booking_id'] = str(result.inserted_id)  # append booking_id after it is generated

    if request.json.get("booking_type") is not None:
        # saga_orchestrator(payload)
        del payload['_id']

        payload['transaction'] = "commit"

        write_transaction({"Transaction": "TRANSACTION STARTED",
                           "Booking ID": payload['booking_id'],
                           "Customer ID": request.json.get("customer_id")})

        publisher(queue="flight", message=payload)

    response = {
        "inserted_id": str(result.inserted_id),
        "acknowledged": result.acknowledged
    }

    return response, 201


if __name__ == "__main__":
    app.run(host=config['host'], port=config['port'])
