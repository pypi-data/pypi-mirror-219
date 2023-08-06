"""
This library provides an easy way to interact with Pub/Sub API.

"""


from google.cloud import pubsub_v1


def write_message(project_id, topic_id, message_str, status, joiner_id):
    """
    Publish a message in Pub Sub.

    Parameters:
    ----------
        project_id: The ID of the gcp project where you want to publish a message.
        topic_id: The topic name where you want to publish the message.
        message_str: The message string to publish.
        status and joinerId: Attributes for the message.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    message = message_str.encode("utf-8")

    future = publisher.publish(
        topic_path, message, status=str(status), joinerId=str(joiner_id)
    )

    result = future.result()

    return result
