import time
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from browser_monitor import BrowserProcessMonitor
import boto3
import logging


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



chrome_driver_path = "web_drivers/chromedriver_win32/chromedriver.exe"
service = Service(chrome_driver_path)

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
# exclude switches for automation extension and enable developer mode and add a localhost:8989
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--remote-debugging-port=8989")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.netflix.com")
driver_pid = driver.service.process.pid
# Create an instance of ProcessMonitorInterface
browser_monitor = BrowserProcessMonitor()

def listen_for_messages():
    while True:
        try:
            # Receive messages from the queue
            response = sqs_client.receive_message(
                QueueUrl=ssqUrl,
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )

            # Process received messages
            messages = response.get('Messages', [])

            if len(messages) > 0:
                logging.info("Messages in Queue: %s", len(messages))
                # Extract message body, group ID, and attributes
                message = messages[0]
                message_body = message['Body']
                message_attributes = message['MessageAttributes']

                return message_body, message_attributes

        except Exception as e:
            logging.error("An error occurred: %s", str(e))


run_browser = True
while run_browser:
    if not browser_monitor.pid_is_running(driver_pid):
        run_browser = False
        print("Browser closed")
        driver.quit()
        break

    # Check for received messages
    message_body, message_attributes = listen_for_messages()
    print("Received Message Body:", message_body)
    print("Message Attributes:", message_attributes)

    if message_body == "pickAaron":
        try:
            # Find and click on the profile name element
            profile_name_element = driver.find_element(By.CLASS_NAME, "profile-name")
            profile_name_element.click()
            print("Clicked on profile: Aaron")
        except Exception as e:
            print("Error clicking on profile:", str(e))

    # Check if the message_attribute is 'mediaLink'
    if message_attributes['MessageType']['StringValue'] == "MediaLink":
        # Your code logic for handling 'mediaLink' group ID
        new_url = message_body
        # Navigate to the new URL on the same tab
        driver.get(new_url)

    elif message_attributes['MessageType']['StringValue'] == "mediaControl":
        if (message_body == "play"):
            # Simulate pressing the space bar to play/pause the video
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
            print("Pressed space bar")


    time.sleep(1)






