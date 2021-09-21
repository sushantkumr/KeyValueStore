# KeyValueStore
A simple flask REST service to store key value pairs.

### Functions
• get: To fetch the value of a Key

• set: To set a Key Value pair

• search: To search if a Key starts or ends with a pattern

### Local development

• To run the project via Docker, run the following commands:

    1. docker build --tag key-value-server .
    2. docker run -p 80:80 key-value-server

• Access the APIs at `http://0.0.0.0/`

### Deploy on Cloud (AWS)
• If you have AWS configured on your local system then follow this guide for deployment

• Install terraform on your system

• Run the following commands in order to deploy:

    1. terraform plan
    2. terraform apply
