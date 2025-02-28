import sys
import os

sys.path.append('/Users/administrator/Desktop/ds-practice-2025/utils/pb')

from utils.pb.fraud_detection import fraud_detection_pb2


import threading
import queue
import grpc
from flask import Flask, request
from flask_cors import CORS
import json
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
fraud_detection_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, fraud_detection_path)
import fraud_detection_pb2 as fraud_pb2
import fraud_detection_pb2_grpc as fraud_grpc

transaction_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, transaction_path)
import transaction_verification_pb2 as transaction_pb2
import transaction_verification_pb2_grpc as transaction_grpc

suggestions_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_path)
import suggestions_pb2 as suggestions_pb2
import suggestions_pb2_grpc as suggestions_grpc


def greet(name='Guest'):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_grpc.HelloServiceStub(channel)
        response = stub.SayHello(fraud_pb2.HelloRequest(name=name))
    return response.greeting


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


def call_fraud_detection(order_data, queue):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_grpc.FraudDetectionStub(channel)
        response = stub.CheckFraud(fraud_pb2.OrderRequest(
            user_name=order_data['user_name'],
            card_number=order_data['card_number'],
            items=[fraud_pb2.Item(name=item['name'], quantity=item['quantity']) for item in order_data['items']],
        ))
        queue.put(('fraud', response.is_fraudulent))


def call_transaction_verification(order_data, queue):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_grpc.TransactionVerificationStub(channel)
        response = stub.VerifyTransaction(transaction_pb2.OrderRequest(
            user_name=order_data['user_name'],
            card_number=order_data['card_number'],
            items=[transaction_pb2.Item(name=item['name'], quantity=item['quantity']) for item in order_data['items']]
        ))
        queue.put(('transaction', response.is_valid))


def call_suggestions(order_data, queue):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_grpc.SuggestionsStub(channel)
        response = stub.GetSuggestions(suggestions_pb2.OrderRequest(
            user_name=order_data['user_name'],
            items=[suggestions_pb2.Item(name=item['name'], quantity=item['quantity']) for item in order_data['items']]
        ))
        queue.put(('suggestions', response.suggested_books))


@app.route('/', methods=['GET'])
def index():
    return greet(name='orchestrator')


@app.route('/checkout', methods=['POST'])
def checkout():
    request_data = json.loads(request.data)
    logger.info("Received request: %s", request_data)
    if 'user' not in request_data or 'creditCard' not in request_data or 'items' not in request_data:
        return {'error': {'code': '400', 'message': 'Missing required fields'}}, 400

    user = request_data['user']
    card = request_data['creditCard']
    items = request_data['items']

    order_id = str(uuid.uuid4())
    order_data = {
        'user_name': user.get('name', 'Unknown'),
        'card_number': card.get('number', ''),
        'items': items
    }

    result_queue = queue.Queue()
    threads = [
        threading.Thread(target=call_fraud_detection, args=(order_data, result_queue)),
        threading.Thread(target=call_transaction_verification, args=(order_data, result_queue)),
        threading.Thread(target=call_suggestions, args=(order_data, result_queue))
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    results = {result_queue.get() for _ in range(3)}
    fraud_result = results.get('fraud', False)
    transaction_result = results.get('transaction', False)
    suggestions_result = results.get('suggestions', [])

    status = 'Order Rejected' if fraud_result or not transaction_result else 'Order Approved'
    order_response = {
        'orderId': order_id,
        'status': status,
        'suggestedBooks': [{'title': book.title, 'author': book.author} for book in suggestions_result]
    }
    logger.info("Response: %s", order_response)
    return order_response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
