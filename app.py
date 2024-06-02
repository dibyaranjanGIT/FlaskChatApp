from flask import Flask, request, jsonify, render_template
import boto3
import json
import os

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# Initialize Boto3 client for Bedrock
client = boto3.client(
    'bedrock-runtime',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


@app.route('/')
def index():
    return "Welcome to the Flask Chat App with Bedrock!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Call Bedrock service to interact with Mistral 7B Instruct model
    response = client.invoke_endpoint(
        EndpointName='your_bedrock_endpoint',  # Replace with your actual endpoint name
        ContentType='application/json',
        Body=json.dumps({
            'input': user_input,
            'parameters': {
                'model': 'mistral-7b-instruct'  # Specify the Mistral 7B Instruct model
            }
        })
    )

    result = response['Body'].read().decode('utf-8')
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(debug=True)
