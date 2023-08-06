import boto3

class SnsOperations:

    def publish(self, topic_arn, message):
        boto3.Session().client(service_name='sns').publish(
            TopicArn=topic_arn,
            Message=message
        )



