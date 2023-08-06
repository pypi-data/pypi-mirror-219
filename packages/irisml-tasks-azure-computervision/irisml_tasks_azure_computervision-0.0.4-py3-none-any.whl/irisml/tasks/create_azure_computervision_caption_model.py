import dataclasses
import logging
import urllib.parse
import torch
import irisml.core
from irisml.tasks.create_azure_computervision_classification_model import AzureComputerVisionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Computer Vision Caption Model.

    This task creates a model that generates a caption of an image using Azure Computer Vision API.

    Model input is List[Union[PIL.Image.Image, torch.Tensor]]. Output is a List[str].

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if not self.config.endpoint.startswith('https://'):
            raise ValueError('endpoint must start with https://')

        model = AzureComputervisionCaptionModel(self.config.endpoint, self.config.api_key)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


class AzureComputervisionCaptionModel(AzureComputerVisionModel):
    def get_url(self, endpoint):
        return urllib.parse.urljoin(endpoint, '/computervision/imageanalysis:analyze?api-version=2023-04-01-preview&features=caption')

    def parse_response(self, response_body):
        return response_body['captionResult']['text']
