"""
SQS consumer
"""

import os
import boto3
import time
import traceback
from typing import List

from .error import SQSException
from .message import Message


class Consumer:
    """
    SQS consumer implementation.
    """

    def __init__(
        self,
        queue_url,
        region=None,
        sqs_client=None,
        attribute_names=[],
        message_attribute_names=[],
        batch_size=1,
        wait_time_seconds=1,
        visibility_timeout_seconds=None,
        polling_wait_time_ms=0
    ):
        self.queue_url = queue_url
        self.attribute_names = attribute_names
        self.message_attribute_names = message_attribute_names

        if not 1 <= batch_size <= 10:
            raise ValueError(
                "Batch size should be between 1 and 10, both inclusive")
        self.batch_size = batch_size

        self.wait_time_seconds = wait_time_seconds
        self.visibility_timeout_seconds = visibility_timeout_seconds
        self.polling_wait_time_ms = polling_wait_time_ms
        if region:
            self._sqs_client = sqs_client or boto3.client(
                "sqs", region_name=region)
        elif "AWS_DEFAULT_REGION" in os.environ:
            # use boto3 default region
            self._sqs_client = sqs_client or boto3.client(
                "sqs", region_name=os.environ["AWS_DEFAULT_REGION"])
        else:
            raise Exception("Please specify the region parameter or set \
                            AWS_DEFAULT_REGION env variable.")
        self._running = False

    def handle_message(self, message: Message):
        """
        Called when a single message is received.
        Write your own logic for handling the message
        by overriding this method.

        Note:
            * If `batch_size` is greater than 1,
              `handle_message_batch(message)` is called instead.
            * Any unhandled exception will be available in
              `handle_processing_exception(message, exception)` method.
        """
        ...

    def handle_message_batch(self, messages: List[Message]):
        """
        Called when a message batch is received.
        Write your own logic for handling the message batch
        by overriding thismethod.

        Note:
            * If `batch_size` equal to 1, `handle_message(message)`
              is called instead.
            * Any unhandled exception will be available in
              `handle_batch_processing_exception(message, exception)` method.
        """
        ...

    def handle_processing_exception(self, message: Message, exception):
        """
        Called when an exception is thrown while processing a message
        including messsage deletion from the queue.

        By default, this prints the exception traceback.
        Override this method to write any custom logic.
        """
        traceback.print_exc()

    def handle_batch_processing_exception(
        self, messages: List[Message], exception
    ):
        """
        Called when an exception is thrown while processing a message batch
        including messsage batch deletion from the queue.

        By default, this prints the exception traceback.
        Override this method to write any custom logic.
        """
        traceback.print_exc()

    def start(self):
        """
        Start the consumer.
        """
        # TODO: Figure out threading/daemon
        self._running = True
        while self._running:
            response = self._sqs_client.receive_message(
                **self._sqs_client_params)

            if not response.get("Messages", []):
                self._polling_wait()
                continue

            messages = [
                Message.parse(message_dict)
                for message_dict in response["Messages"]
            ]

            if self.batch_size == 1:
                self._process_message(messages[0])
            else:
                self._process_message_batch(messages)

    def stop(self):
        """
        Stop the consumer.
        """
        # TODO: There's no way to invoke this other than a separate thread.
        self._running = False

    def _process_message(self, message: Message):
        try:
            self.handle_message(message)
            self._delete_message(message)
        except Exception as exception:
            self.handle_processing_exception(message, exception)
        finally:
            self._polling_wait()

    def _process_message_batch(self, messages: List[Message]):
        try:
            self.handle_message_batch(messages)
            self._delete_message_batch(messages)
        except Exception as exception:
            self.handle_batch_processing_exception(messages, exception)
        finally:
            self._polling_wait()

    def _delete_message(self, message: Message):
        try:
            self._sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message.ReceiptHandle
            )
        except Exception:
            raise SQSException("Failed to delete message")

    def _delete_message_batch(self, messages: List[Message]):
        try:
            self._sqs_client.delete_message_batch(
                QueueUrl=self.queue_url,
                Entries=[
                    {
                        "Id": message.MessageId,
                        "ReceiptHandle": message.ReceiptHandle
                    }
                    for message in messages
                ]
            )
        except Exception:
            raise SQSException("Failed to delete message batch")

    @property
    def _sqs_client_params(self):
        params = {
            "QueueUrl": self.queue_url,
            "AttributeNames": self.attribute_names,
            "MessageAttributeNames": self.message_attribute_names,
            "MaxNumberOfMessages": self.batch_size,
            "WaitTimeSeconds": self.wait_time_seconds,
        }
        if self.visibility_timeout_seconds is not None:
            params["VisibilityTimeout"] = self.visibility_timeout_seconds

        return params

    def _polling_wait(self):
        time.sleep(self.polling_wait_time_ms / 1000)
