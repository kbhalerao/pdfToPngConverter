# pdfToPngConverter
An experiment with Lambda and API Gateway

Here's a simple Lambda that executes on a container, is attached to an API Gateway trigger, and converts a Base64-encoded PDF  into a list of Base64-encoded PNGs. Since we are using the API Gateway, this function executes synchronously. 

Installation:
- Clone this repo
- Build the Docker image with something like `docker build -t pdf2img .`
- Set up a *private* Elastic Container Registry with AWS in `us-east-1`: Nothing else worked as of 9/12/21. 
- Log the Docker CLI to ECR, and tag and push the container to ECR (look at the Push Commands on ECR)
- Create a new Lambda with this container, and wire up an API trigger. 
- Look at the tests on how to use this API. 

