from datetime import datetime
from typing import Callable, Dict, Any
from typeguard import typechecked

from openai_wrapper.config import Config
import logging

logging.basicConfig(level=logging.INFO)


def _preprocess_text(text: str) -> str:
    """
    Basic implementation of preprocessing the texts.

    Args:
        text: The text to preprocess

    Returns:
        The preprocessed text
    """
    return text


def _process_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic implementation of processing the response.

    Args:
        response: The response to preprocess

    Returns:
        The preprocessed response
    """
    return response


@typechecked
class Embeddings:
    """
    A wrapper for the OpenAI Embeddings API

    Attributes:
        use_case_name: name of the use case so it can be used as a collection name in MongoDB (e.g. "Q&A", "Quiz_Generation")
        config: A Config object
        model: The model to use for the embeddings
        model_params: A dictionary of parameters used to create the embeddings
        experiment_metadata: A dictionary of pre-defined metadata in project_experiment.ini about the experiment
        project_metadata: A dictionary of pre-defined metadata in project.ini about the project
        extra_params: Any extra parameters that should be stored in the MongoDB document
    """

    def __init__(self,
                 use_case_name: str,
                 config: Config,
                 model: str = "text-embedding-ada-002",
                 experiment_metadata: Dict[str, Any] = None,
                 project_metadata: Dict[str, Any] = None,
                 extra_params: Dict[Any, Any] = None):

        logging.info(f"Initializing Embeddings object for collection {use_case_name}")
        logging.info(f"Embeddings Model: {model}")

        self.use_case_name = use_case_name
        self.config = config
        self.mongo_client = config.mongo_client
        self.async_mongo_client = config.async_mongo_client
        self.openai_client = config.openai_client

        self.model_params = {
            "model": model,
            "input": [],
        }

        self.experiment_metadata = experiment_metadata
        self.project_metadata = project_metadata
        self.extra_params = extra_params

    def create(self,
               text: str,
               preprocess_text: Callable = _preprocess_text,
               process_response: Callable = _process_response,
               preprocess_texts_args: Dict[Any, Any] = None,
               process_response_args: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """
        Create an embeddings request and store it in MongoDB

        Args:
            text: The texts to use for the embeddings
            preprocess_text: A function that preprocesses the texts
            process_response: A function that processes the response
            preprocess_texts_args: A dictionary of arguments to pass to the preprocess_texts function
            process_response_args: A dictionary of arguments to pass to the process_response function

        Returns:
            A dictionary containing the embeddings request and response
        """

        if preprocess_texts_args is None:
            preprocess_texts_args = {}
        if process_response_args is None:
            process_response_args = {}

        preprocessed_text = preprocess_text(text, **preprocess_texts_args)
        self.model_params["input"] = [preprocessed_text]
        response = self.openai_client.Embedding.create(**self.model_params)

        if process_response is not None:
            response = process_response(response, **process_response_args)

        document = {
            "input_text": preprocessed_text,
            "response": response,
            "openai_response": response.__dict__['_previous'],
            "model_params": self.model_params,
            "created_at": str(datetime.utcnow()),
            "experiment_metadata": self.experiment_metadata,
            "project_metadata": self.project_metadata,
        }

        if self.extra_params is not None:
            document.update(self.extra_params)

        mongo_db = self.mongo_client[self.config.mongo_db_name]
        mongo_collection = mongo_db[self.use_case_name]
        mongo_collection.insert_one(document)

        return document