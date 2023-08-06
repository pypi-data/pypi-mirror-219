import datetime
import io
import json
from typing import Dict, Optional, Union

import avro.schema as schema
from arcane.firebase import generate_token
from avro.io import BinaryEncoder, DatumWriter
from google.cloud.pubsub import SchemaServiceClient
from google.cloud.pubsub_v1 import PublisherClient as GooglePubSubClient
from google.oauth2 import service_account
from google.pubsub_v1.types import Encoding
from typing_extensions import Literal


class Client(GooglePubSubClient):
    def __init__(self, adscale_key=None):
        credentials = service_account.Credentials.from_service_account_file(adscale_key)
        super().__init__(credentials=credentials)

    def push_to_topic(self, project: str,
                      topic_name: str,
                      parameters: dict,
                      firebase_api_key: str = None,
                      await_response: bool = False,
                      attributes: Union[Dict, None] = None):
        """ Add the message to the given topic and if needed, generates  a token to be sent along the message
        to allow authorization"""
        if firebase_api_key:
            token = generate_token(firebase_api_key)
            message = json.dumps({'parameters': parameters, 'token': token}).encode('utf-8')
        else:
            message = json.dumps({'parameters': parameters}).encode('utf-8')

        topic_path = self.topic_path(project, topic_name)
        if attributes is not None:
            future = self.publish(topic_path, message, **attributes)
        else:
            future = self.publish(topic_path, message)
        if await_response:
            future.result()
        return future

    def pubsub_publish_pf_monitoring(self,
                                    topic: str,
                                    project_id:str,
                                    monitoring_id: str,
                                    step: str,
                                    entity_id: str,
                                    status: Literal['start', 'done', 'error'],
                                    error_message: Optional[str] = None):
        """ publish a message for product flow monitoring"""

        parameters = dict(
            entity_id=entity_id,
            monitoring_id=monitoring_id,
            step=step,
            status=status
        )
        if error_message is not None:
            parameters['error_message'] = error_message

        self.push_to_topic(project=project_id,
                    topic_name=topic,
                    parameters=parameters,
                    await_response=True)
        print(f"Published {status} message for entity {entity_id} and monitoring_id {monitoring_id}")

    def publish_with_schema(
      self,
      project:str,
      topic_name:str,
      message:dict,
      await_response:bool=False
    ):
        """Publishes a message to a topic with a schema.

        Args:
            project (str): Project ID of the project that the topic belongs to
            topic_name (str): Name of the topic to publish to
            message (dict): Message to publish
            await_response (bool, optional): Whether to await for the future to resolve. Defaults to False.

        Raises:
            ValueError: If no encoding is specified in the topic

        Returns:
            Future: Future object
        """
        schema_client = SchemaServiceClient()
        topic_path = self.topic_path(project, topic_name)
        topic = self.get_topic(
            topic=topic_path
        )
        schema_path = topic.schema_settings.schema
        result = schema_client.get_schema(request={"name": schema_path}).definition
        avro_schema = schema.parse(result)
        writer = DatumWriter(avro_schema)
        bout = io.BytesIO()
        encoding = topic.schema_settings.encoding


        if encoding == Encoding.BINARY:
            encoder = BinaryEncoder(bout)
            writer.write(message, encoder)
            data = bout.getvalue()
        elif encoding == Encoding.JSON:
            data_str = json.dumps(message)
            data = data_str.encode("utf-8")
        else:
            raise ValueError(f"No encoding specified in {topic_path}. Abort.")
        
        future = self.publish(topic_path, data)
        if await_response:
            future.result()
        return future