import boto3

# Replace with your topic ARN
topic_arn = "arn:aws:sns:<region>:<account-id>:<topic-name>"


def subscribe(endpoint):
    """
    Subscribes the provided endpoint to the SNS topic and handles confirmation.

    Args:
        endpoint (str): The URL of your application endpoint to receive messages.

    Returns:
        str: The subscription ARN if successful, otherwise None.
    """

    sns_client = boto3.client('sns')

    try:
        # Subscribe the endpoint to the topic
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='http',  # Assuming HTTP protocol for your endpoint
            Endpoint=endpoint
        )

        subscription_arn = response['SubscriptionArn']
        print(f"Subscription request sent. Subscription ARN: {subscription_arn}")

        # Confirm the subscription using the SubscribeURL from the response
        confirm_url = response['SubscribeURL']
        print(f"Visit this URL to confirm your subscription: {confirm_url}")

        # Simulate user confirmation (replace with actual confirmation logic)
        user_confirmed = True

        if user_confirmed:
            # Send a GET request to the confirmation URL to confirm subscription
            response = boto3.resource('sns').Subscription(subscription_arn).confirm()
            print(f"Subscription confirmed successfully. Status: {response['SubscriptionStatus']}")
            return subscription_arn
        else:
            print("Subscription confirmation not received. Please confirm manually using the provided URL.")
            return None

    except ClientError as error:
        print(f"Subscription failed: {error}")
        return None


if __name__ == "__main__":
    # Replace with your application endpoint URL
    endpoint = "http://your-application.com/sns-endpoint"

    subscription_arn = subscribe(endpoint)

    if subscription_arn:
        print(f"You are now subscribed to the topic. Subscription ARN: {subscription_arn}")
