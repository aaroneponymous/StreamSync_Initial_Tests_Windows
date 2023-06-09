import boto3
import logging
import subprocess
from botocore.exceptions import ClientError

aws_access_key_id = ''
aws_secret_access_key = ''
aws_region_name = ''
ssqUrl = ''

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired log level

# Create an SQS client
sqs_client = boto3.client('sqs', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region_name)


def get_queue_attributes(queue_url, attribute_names):
    """
    Gets attributes for the specified queue.
    """
    try:
        response = sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=attribute_names)
    except ClientError as e:
        logging.error(e)
        return None
    else:
        return response



def listen_for_messages():
    while True:
        try:
            # Receive messages from the queue
            response = sqs_client.receive_message(
                QueueUrl=ssqUrl,
                MaxNumberOfMessages=10
            )

            # Process Received Messages
            messages = response.get('Messages', [])

            if len(messages) > 0:
                logging.info("Messages in Queue: %s", len(messages))
                return messages[0]['Body']

        except Exception as e:
            logging.error("An error occurred: %s", str(e))


def process_message(message):
    message_body = message['Body']
    message_group_id = message['MessageGroupId']
    message_attributes = message['MessageAttributes']
    message_receipt_handle = message['ReceiptHandle']

    logging.info("Received Message: %s", message_body)
    logging.info("Message Group ID: %s", message_group_id)
    logging.info("Message Attributes: %s", message_attributes)

    # Run netflix_chrome.py if message_body == 'startNetflix'
    if message_body == 'startNetflix':
        subprocess.run(["python", "netflix_chrome.py"])

    # Process the message as needed
    # ...

    # Delete the message from the queue
    sqs_client.delete_message(
        QueueUrl=ssqUrl,
        ReceiptHandle=message_receipt_handle
    )

    logging.info("Deleted message with ReceiptHandle: %s", message_receipt_handle)



# Continuously listen for messages
while True:
    try:
        # Receive messages from the queue
        response = sqs_client.receive_message(
            QueueUrl=ssqUrl,
            MaxNumberOfMessages=10,
            AttributeNames=['MessageGroupId']  # Request the MessageGroupId attribute
        )

        # Process Received Messages
        messages = response.get('Messages', [])

        if len(messages) > 0:
            logging.info("Messages in Queue: %s", len(messages))

        for message in messages:
            message_body = message['Body']
            

            logging.info("Received Message: %s", message_body)
          

            # Run netflix_chrome.py if message_body == 'start'
            if message_body == 'startNetflix':
                subprocess.run(["python", "netflix_chrome.py"])

            # Process the message as needed
            # ...

            # Delete the message from the queue
            sqs_client.delete_message(
                QueueUrl=ssqUrl,
                ReceiptHandle=message['ReceiptHandle']
            )

            logging.info("Deleted message with ReceiptHandle: %s", message['ReceiptHandle'])

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
