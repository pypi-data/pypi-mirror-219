import unittest
import unittest.mock
import PIL.Image
import torch
from irisml.tasks.create_azure_computervision_classification_model import Task


class TestCreateAzureComputervisionClassificationModel(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        with unittest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'tagsResult': {'values': [{'name': 'object_name', 'confidence': 0.5}]}}
            model_outputs = outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
            self.assertEqual(model_outputs, [['object_name'], ['object_name']])
