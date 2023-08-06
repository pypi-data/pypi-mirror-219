import datetime
import os
import traceback
import coolname
from dequeai.rest_connect import RestConnect
from dequeai.deque_environment import AGENT_API_SERVICE_URL
import pickle
import multiprocessing
from dequeai.parsing_service import ParsingService
from dequeai.datatypes import Image, Audio, Histogram, BoundingBox2D, Table, DEQUE_GRADIENT_HISTOGRAM
from dequeai.util import MODEL, CODE, DATA, ENVIRONMENT, RESOURCES, TRACKING_ENDPOINT
import requests
import glob
import time
import psutil
import GPUtil
import socket
import types
from IPython.display import display, HTML
from tabulate import tabulate
import numpy as np
import json
from typing import Optional

_RESOURCE_MONITORING_INTERVAL = 60


class ModelCard:

    def __init__(self):
        self._user_name = None
        self._api_key = None
        self._project_name = None
        self._run_id = None
        self._model_name = None
        self._task_category = None
        self._task = None
        self._model_architecture = None
        self._model_description = None
        self._model_version = None
        self._limitations = None
        self._intended_users = None
        self._training_data_size = None
        self._training_data_size_units = None
        self._training_data_description = None
        self._training_data_source = None
        self._training_date = None
        self._license = None
        self._citation = None
        self._dependencies = None
        self._pretrained = None

    def init(self, user_name, api_key, run_id, project_name=None):
        self._user_name = user_name
        self._api_key = api_key
        self._project_name = project_name
        self._run_id = run_id

    def create(self, model_name: str, task_category: str, task: str, model_architecture: str, model_version: str,
               training_date: str, model_license: str, dependencies: list, pretrained: str,
               model_description: Optional[str] = None,
               limitations: Optional[str] = None, intended_users: Optional[str] = None,
               training_data_size: Optional[str] = None,
               training_data_size_units: Optional[str] = None, training_data_description: Optional[str] = None,
               training_data_source: Optional[str] = None,
               citation: Optional[str] = None):
        self.model_name = model_name
        self.task_category = task_category
        self.task = task
        self.model_architecture = model_architecture
        self.model_description = model_description
        self.model_version = model_version
        self.limitations = limitations
        self.intended_users = intended_users
        self.training_data_size = training_data_size
        self.training_data_size_units = training_data_size_units
        self.training_data_description = training_data_description
        self.training_data_source = training_data_source
        self.training_date = training_date
        self.license = model_license
        self.citation = citation
        self.dependencies = dependencies
        self.pretrained = pretrained

        return self

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_dict(self, d):
        self.__dict__ = d

    def from_json(self, j):
        self.__dict__ = json.loads(j)

    @property
    def task_category(self) -> Optional[str]:
        return self.task_category

    @task_category.setter
    def task_category(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("task_category must be a string or None.")
        self.task_category = value

    @property
    def task(self) -> Optional[str]:
        return self.task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("task must be a string or None.")
        self.task = value

    @property
    def model_name(self) -> Optional[str]:
        return self.model_name

    @model_name.setter
    def model_name(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("model_name must be a string or None.")
        self.model_name = value

    @property
    def model_architecture(self) -> Optional[str]:
        return self.model_architecture

    @model_architecture.setter
    def model_architecture(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("model_architecture must be a string or None.")
        self.model_architecture = value

    @property
    def model_description(self) -> Optional[str]:
        return self.model_description

    @model_description.setter
    def model_description(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("model_description must be a string or None.")
        self.model_description = value

    @property
    def model_version(self) -> Optional[str]:
        return self._model_version

    @model_version.setter
    def model_version(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("model_version must be a string or None.")
        self.model_version = value

    @property
    def limitations(self) -> Optional[str]:
        return self.limitations

    @limitations.setter
    def limitations(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("limitations must be a string or None.")
        self.limitations = value

    @property
    def intended_users(self) -> Optional[str]:
        return self.intended_users

    @intended_users.setter
    def intended_users(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("intended_users must be a string or None.")
        self.intended_users = value

    @property
    def training_data_size(self) -> Optional[str]:
        return self.training_data_size

    @training_data_size.setter
    def training_data_size(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("training_data_size must be a string or None.")
        self.training_data_size = value

    @property
    def training_data_size_units(self) -> Optional[str]:
        return self.training_data_size_units

    @training_data_size_units.setter
    def training_data_size_units(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("training_data_size_units must be a string or None.")
        self.training_data_size_units = value

    @property
    def training_data_description(self) -> Optional[str]:
        return self.training_data_description

    @training_data_description.setter
    def training_data_description(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("training_data_description must be a string or None.")
        self.training_data_description = value

    @property
    def training_data_source(self) -> Optional[str]:
        return self.training_data_source

    @training_data_source.setter
    def training_data_source(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("training_data_source must be a string or None.")
        self.training_data_source = value

    @property
    def training_date(self) -> Optional[str]:
        return self.training_date

    @training_date.setter
    def training_date(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("training_date must be a string or None.")
        self.training_date = value

    @property
    def citation(self) -> Optional[str]:
        return self.citation

    @citation.setter
    def citation(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("citation must be a string or None.")
        self.citation = value

    @property
    def license(self) -> Optional[str]:
        return self.license

    @license.setter
    def license(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError("license must be a string or None.")
        self.license = value

    @property
    def dependencies(self) -> Optional[str]:
        return self.dependencies

    @dependencies.setter
    def dependencies(self, value: Optional[str]) -> None:
        if value is not isinstance(value, list):
            raise ValueError("dependencies must be a list")
        self.dependencies = value

    @property
    def pretrained(self) -> Optional[str]:
        return self.pretrained

    @pretrained.setter
    def pretrained(self, value: Optional[str]) -> None:
        if value is not isinstance(value, bool):
            raise ValueError("pretrained must be a boolean")
        self.pretrained = value




class Model:

    def __init__(self):
        self.model_card = None
        self.user_name = None
        self.api_key = None
        self._project_name = None
        self._run_id = None

    def init(self, user_name, api_key, run_id, project_name=None):
        self.user_name = user_name
        self.api_key = api_key
        self._project_name = project_name
        self._run_id = run_id

    def create(self, model, model_card: ModelCard):

        if self.user_name is None:
            raise Exception("Please call dequeai.init(user_name, api_key, project_name) before creating model")
        if model is None:
            raise Exception("Please provide a valid model")
        try:
            import torch
        except ImportError:
            raise ImportError("PyTorch is required for creating model.")
        if model_card is None:
            raise Exception("Please provide a valid model card")

        if not isinstance(model_card, ModelCard):
            raise Exception("Please create a ModelCard object and pass it as an argument")
        # Check if the model is a PyTorch model
        if not isinstance(model, torch.nn.Module):
            raise Exception('Model should be an instance of a PyTorch nn.Module.')

        p2 = multiprocessing.Process(target=self._create_task, args=(model, model_card))
        p2.start()

    def _create_task(self, model, model_card):

        file_name = f"{self._project_name}.pt"
        try:
            import torch
        except ImportError:
            raise ImportError("PyTorch is required for creating model.")

        torch.save(model, file_name)

        dest_path = "users/" + self.user_name + "/projects/" + self._project_name + "/runs/" + self._run_id + "/model/" + file_name

        req_data = {"user_name": self.user_name, "destination_path": dest_path}
        resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/appstore/model/upload/presigned_url/read/",
                             json=req_data)
        res = resp.json()
        #print(res)
        with open(file_name, 'rb') as f:
            files = {'file': (file_name, f)}
            if "fields" in res:
                http_response = requests.post(url=res['url'], data=res['fields'], files=files)
            else:
                # TODO: for google we need a different way to save data
                object_text = f.read()
                headers = {'Content-type': "application/octet-stream"}
                http_response = requests.put(url=res['url'], data=object_text, headers=headers)
            print(http_response)

        req_data = {"user_name": self.user_name,
                    "model_name": self._project_name, "file_url": dest_path, "bucket_name": res['bucket_name'],
                    "bucket_region": res['bucket_region'],
                    "project_name": self._project_name, "run_id": self._run_id, "model_card": model_card.to_dict()}
        resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/appstore/model/create/",
                             json=req_data)
        res = resp.json()
        print(res)
        # we record the meta data

    def load(self, model_name, run_id=None):
        if self.user_name is None:
            raise Exception("Please call dequeai.init(user_name, api_key, project_name) before loading model")
        req_data = {
            "user_name": self.user_name,
            "run_id": run_id,
            "model_name": model_name
        }
        resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/artifact/metadata/read/", json=req_data)
        metadata = resp.json()

        if not metadata:
            print("No metadata found for the given run_id and user_name.")
            return

        artifacts = metadata["artifacts"]

        # Download the artifacts using the artifact URIs
        for artifact in artifacts:

            if artifact['artifact_type'] == None:
                req_data = {
                    "user_name": self.user_name,
                    "complete_object_path": artifact['artifact_uri']
                }
                resp = requests.post(url=AGENT_API_SERVICE_URL + "/fex/drive/contents/download/presigned_url/read/",
                                     json=req_data)
                res = resp.json()
                # Download the artifact using the pre-signed URL
                http_response = requests.get(url=res["url"])
                file_name = os.path.basename(artifact['artifact_uri'])
                with open(file_name, "wb") as f:
                    f.write(http_response.content)
                print(f"Downloaded artifact '{file_name}'")

    def _validate_data(self, data):
        new_data = {}
        for key, value in data.items():
            if key is None:
                raise ValueError("Key cannot be None")

            if isinstance(value, dict):
                new_data[key] = self._validate_data(value)
            else:
                if isinstance(value, (Audio, BoundingBox2D, Histogram, Table, Image)) or \
                        type(value) in types.__builtins__.values():
                    new_data[key] = value
                elif isinstance(value, np.generic):  # Check if the value is a numpy type
                    new_data[key] = self._convert_numpy_to_python(value)  # Convert numpy to Python scalar
                else:
                    raise ValueError(
                        "Invalid type in dictionary. Allowed values include builtin types and Deque data types " + str(
                            type(value)) + " " + str(value.__class__.__module__))
        return new_data


if __name__ == "__main__":
    mc = ModelCard()
    mc.__setattr__("model_name", "test")
    print(mc.model_name)
    print(mc)
    # mc.init("test", "test", "test")
