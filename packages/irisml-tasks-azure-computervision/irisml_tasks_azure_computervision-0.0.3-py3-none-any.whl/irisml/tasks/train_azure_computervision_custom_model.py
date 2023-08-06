import concurrent.futures
import dataclasses
import io
import json
import logging
import time
import typing
import urllib.parse
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient, ContentSettings
import requests
import tenacity
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Train Azure Computer Vision Custom Model.

    This task uploads a dataset to the provided Azure Storage Blob container, trains a custom model using Azure Computer
    Vision API, and deletes the dataset from the container.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        task_type (str): Task type. Must be one of 'classification_multiclass' or 'object_detection'.
        azure_storage_blob_container_url (str): Azure Storage Blob container URL. Make sure the Computer Vision API resrouce has access to this storage.
        budget_in_hours (int): Budget in hours.
        keep_dataset (bool): Keep the dataset in the container after training.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        class_names: typing.List[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        task_type: typing.Literal['classification_multiclass', 'object_detection']
        azure_storage_blob_container_url: str
        budget_in_hours: int = 1
        keep_dataset: bool = False

    @dataclasses.dataclass
    class Outputs:
        model_name: str

    def execute(self, inputs):
        self._uvs_client = UVSClient(self.config.endpoint, self.config.api_key)
        dataset_name = f'dataset_{uuid.uuid4()}'
        logger.info(f"Uploading dataset to Azure Storage Blob. {dataset_name=}")
        self._upload_dataset(inputs.dataset, dataset_name, inputs.class_names)

        model_name = f'model_{uuid.uuid4()}'
        logger.info(f"Training model. {model_name=}")
        start = time.time()
        self._train_model(dataset_name, model_name)
        logger.info(f"Training model finished. {model_name=}. Elapsed time: {time.time() - start:.2f} seconds")
        if not self.config.keep_dataset:
            logger.info('Deleting dataset from Azure Storage Blob...')
            self._delete_dataset(dataset_name)

        return self.Outputs(model_name=model_name)

    def dry_run(self, inputs):
        return self.Outputs(model_name=str(uuid.uuid4()))

    def _upload_dataset(self, dataset, dataset_name, class_names):
        container_client = ContainerClient.from_container_url(self.config.azure_storage_blob_container_url, credential=DefaultAzureCredential())

        logger.info(f"Uploading {len(dataset)} images to Azure Storage Blob...")
        targets = []
        images = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i, (image, target) in enumerate(dataset):
                targets.append(target)
                images.append({'id': i + 1, 'width': image.width, 'height': image.height, 'file_name': f'{i}.jpg'})
                with io.BytesIO() as f:
                    image.save(f, format='JPEG')
                    image_bytes = f.getvalue()
                executor.submit(self._upload_file, f'{dataset_name}/{i}.jpg', image_bytes, 'image/jpeg', container_client)

        # Construct annotations file
        if self.config.task_type == 'classification_multiclass':
            annotations = [{'id': i + 1, 'image_id': i + 1, 'category_id': int(target) + 1} for i, target in enumerate(targets)]
        elif self.config.task_type == 'object_detection':
            annotation_index = 1
            annotations = []
            for i, target in enumerate(targets):
                for t in target:
                    bbox = [float(t[1]), float(t[2]), float(t[3]) - float(t[1]), float(t[4]) - float(t[2])]
                    annotations.append({'id': annotation_index, 'image_id': i + 1, 'category_id': int(t[0]) + 1, 'bbox': bbox})
                    annotation_index += 1
        else:
            raise ValueError(f"Invalid task_type: {self.config.task_type}")

        # Make dataset json file
        coco_dataset = {'info': {},
                        'categories': [{'id': i + 1, 'name': name} for i, name in enumerate(class_names)],
                        'images': images,
                        'annotations': annotations}

        coco_dataset_json = json.dumps(coco_dataset, indent=2)
        self._upload_file(f'{dataset_name}/dataset.json', coco_dataset_json, 'application/json', container_client)

        json_url = f'{self.config.azure_storage_blob_container_url}/{dataset_name}/dataset.json'
        self._uvs_client.register_dataset(dataset_name, self.config.task_type, json_url)

    def _delete_dataset(self, dataset_name):
        assert dataset_name
        container_client = ContainerClient.from_container_url(self.config.azure_storage_blob_container_url, credential=DefaultAzureCredential())

        for blob in container_client.list_blobs(name_starts_with=dataset_name):
            container_client.delete_blob(blob)

        self._uvs_client.unregister_dataset(dataset_name)

    def _train_model(self, dataset_name, model_name):
        self._uvs_client.create_model(dataset_name, model_name, self.config.task_type, self.config.budget_in_hours)
        logger.info(f"Training request sent. Waiting for training to complete... Training budget is {self.config.budget_in_hours} hours.")
        status = None
        while not status or status.lower() in ['notstarted', 'training']:
            time.sleep(60)
            status = self._uvs_client.get_model_status(model_name)

        if status.lower() == 'failed':
            raise RuntimeError(f"Training failed. {model_name=}")

    @tenacity.retry(stop=tenacity.stop_after_attempt(5))
    def _upload_file(self, blob_name, data, content_type, container_client):
        try:
            blob_client = container_client.get_blob_client(blob_name)
            content_settings = ContentSettings(content_type=content_type)
            blob_client.upload_blob(data, content_settings=content_settings, timeout=300, overwrite=False)
        except Exception as e:
            logger.warning(f"Failed to upload {blob_name} to Azure Storage Blob. {e=}")
            raise


class UVSClient:
    def __init__(self, endpoint, api_key):
        self._endpoint = endpoint
        self._headers = {'Ocp-Apim-Subscription-Key': api_key}

    def register_dataset(self, dataset_name, task_type, file_url):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/datasets/{dataset_name}?api-version=2023-04-01-preview')
        annotation_kind = {'classification_multiclass': 'imageClassification', 'object_detection': 'imageObjectDetection'}[task_type]
        response = requests.put(url, headers=self._headers, json={'annotationKind': annotation_kind, 'annotationFileUris': [file_url]}, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()

    def create_model(self, dataset_name, model_name, task_type, budget_in_hours):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/models/{model_name}?api-version=2023-04-01-preview')
        model_kind = {'classification_multiclass': 'GenericClassifier', 'object_detection': 'GenericDetector'}[task_type]
        response = requests.put(url, headers=self._headers,
                                json={'trainingParameters': {'timeBudgetInHours': budget_in_hours, 'trainingDatasetName': dataset_name, 'modelKind': model_kind}}, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()

    def get_model_status(self, model_name):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/models/{model_name}?api-version=2023-04-01-preview')
        response = requests.get(url, headers=self._headers, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()
        return response_json['status']

    def unregister_dataset(self, dataset_name):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/datasets/{dataset_name}?api-version=2023-04-01-preview')
        response = requests.delete(url, headers=self._headers, timeout=60)
        response.raise_for_status()
