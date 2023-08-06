import dataclasses
import logging
import urllib.parse
import requests
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Delete Azure Computer Vision Custom Model.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        model_name (str): Custom model name to delete.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        model_name: str

    def execute(self, inputs):
        url = urllib.parse.urljoin(self.config.endpoint, f'/computervision/models/{self.config.model_name}?api-version=2023-04-01-preview')
        logger.info(f"Deleting model {self.config.model_name} on {self.config.endpoint}...")
        response = requests.delete(url, headers={'Ocp-Apim-Subscription-Key': self.config.api_key}, timeout=60)
        response.raise_for_status()
        return self.Outputs()
