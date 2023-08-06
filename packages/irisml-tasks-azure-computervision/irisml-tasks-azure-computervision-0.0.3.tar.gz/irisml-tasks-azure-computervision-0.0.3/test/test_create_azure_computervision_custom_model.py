import unittest
import unittest.mock
import PIL.Image
import torch
from irisml.tasks.create_azure_computervision_custom_model import Task


class TestCreateAzureComputervisionCustomModel(unittest.TestCase):
    def test_classification(self):
        outputs = Task(Task.Config('https://example.com/', 'fake_api_key', 'fake_model_name', 'classification_multiclass')).execute(Task.Inputs(['label0', 'label1']))
        self.assertIsInstance(outputs.model, torch.nn.Module)
        model = outputs.model

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.side_effect = [
                    {'customModelResult': {'tagsResult': {'values': [{'name': 'label0', 'confidence': 0.25}]}}},
                    {'customModelResult': {'tagsResult': {'values': [{'name': 'label1', 'confidence': 0.5}]}}}
                ]
            model_outputs = model([PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (128, 128))])

        self.assertEqual(model_outputs.shape, torch.Size([2, 2]))
        self.assertEqual(model_outputs.tolist(), [[0.25, 0.0], [0.0, 0.5]])

    def test_object_detection(self):
        outputs = Task(Task.Config('https://example.com/', 'fake_api_key', 'fake_model_name', 'object_detection')).execute(Task.Inputs(['label0', 'label1']))
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.side_effect = [
                    {'metadata': {'width': 100, 'height': 100},
                        'customModelResult': {'objectsResult': {'values': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label0', 'confidence': 0.25}]}]}}},
                    {'metadata': {'width': 200, 'height': 200},
                        'customModelResult': {'objectsResult': {'values': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label1', 'confidence': 0.5}]}]}}}
                ]
            model_outputs = outputs.model([PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (200, 200))])

        self.assertEqual(len(model_outputs), 2)
        self.assertEqual(model_outputs[0].tolist(), [[0, 0.25, 0, 0, 1, 1]])
        self.assertEqual(model_outputs[1].tolist(), [[1, 0.5, 0, 0, 0.5, 0.5]])
