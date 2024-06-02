from flask import Flask, request, jsonify, render_template
import boto3
import json
import os

# Function to get secrets from AWS Secrets Manager
def get_secret(secret_name):
    region_name = os.getenv('AWS_REGION', 'ap-south-1')  # Default region if not set

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Load secrets
secrets = get_secret('bedrock_secret')
AWS_ACCESS_KEY = secrets['AWS_ACCESS_KEY']
AWS_SECRET_KEY = secrets['AWS_SECRET_KEY']
AWS_REGION = secrets['AWS_REGION']


app = Flask(__name__)


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
        EndpointName='mistral-7b-instruct',  # Replace with your actual endpoint name
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
