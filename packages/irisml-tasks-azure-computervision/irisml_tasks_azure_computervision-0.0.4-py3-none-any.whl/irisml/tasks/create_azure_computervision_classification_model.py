import dataclasses
import io
import logging
import typing
import urllib.parse
import PIL.Image
import requests
import tenacity
import torch
import torchvision.transforms.functional
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Computer Vision Caption Model.

    This task creates a model that generates a caption of an image using Azure Computer Vision API.

    Model input is (image: Union[PIL.Image.Image, torch.Tensor], targets: Any). Output is a list of str.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
    """
    VERSION = '0.1.1'

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

        model = AzureComputervisionClassificationModel(self.config.endpoint, self.config.api_key)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


def _should_retry(exception):
    if isinstance(exception, requests.exceptions.RequestException):
        response = getattr(exception, 'response', None)
        if response is not None and (response.status_code == 429 or response.status_code >= 500):
            return True
        if isinstance(exception, requests.exceptions.ConnectionError):
            return True
    return False


class AzureComputerVisionModel(torch.nn.Module):
    def __init__(self, endpoint, api_key):
        super().__init__()
        self._endpoint = endpoint
        self._api_key = api_key
        self._url = self.get_url(endpoint)

    def forward(self, inputs) -> typing.List[str]:
        responses = []
        for image in inputs:
            image_bytes = self._get_image_bytes(image)
            response = None
            try:
                response = self._request(image_bytes)
            except Exception:
                logger.exception("Failed to request to Azure Computer Vision API")
            responses.append(response)
        return self.collate_result(responses)

    def get_url(self, endpoint):
        raise NotImplementedError

    def parse_response(self, response_body):
        raise NotImplementedError

    def collate_result(self, batch):
        return [b if b else '' for b in batch]

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def _request(self, image_bytes):
        headers = {'Ocp-Apim-Subscription-Key': self._api_key, 'Content-Type': 'image/png'}
        response = None
        try:
            response = requests.post(self._url, headers=headers, data=image_bytes)
            response.raise_for_status()
        except Exception as e:
            if response:
                logger.error(f"Failed to request to Azure Computer Vision API: {e} {response.content}")
            raise

        return self.parse_response(response.json())

    @staticmethod
    def _get_image_bytes(image: typing.Union[PIL.Image.Image, torch.Tensor]) -> bytes:
        if isinstance(image, torch.Tensor):
            image = torchvision.transforms.functional.to_pil_image(image)

        if isinstance(image, PIL.Image.Image):
            with io.BytesIO() as f:
                image.save(f, format='PNG')
                return f.getvalue()

        raise TypeError(f"image must be PIL.Image.Image or torch.Tensor, but got {type(image)}")


class AzureComputervisionClassificationModel(AzureComputerVisionModel):
    def get_url(self, endpoint):
        return urllib.parse.urljoin(endpoint, '/computervision/imageanalysis:analyze?api-version=2023-04-01-preview&features=tags')

    def parse_response(self, response_body):
        return [t['name'] for t in response_body['tagsResult']['values']]
