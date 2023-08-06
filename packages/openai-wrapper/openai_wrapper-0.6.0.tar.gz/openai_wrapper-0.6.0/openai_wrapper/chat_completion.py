from datetime import datetime
from typing import Callable, Dict, Any, List, Union
from typeguard import typechecked

from openai_wrapper.config import Config
import logging

logging.basicConfig(level=logging.INFO)


def _preprocess_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Basic implementation of preprocessing the messages.

    Args:
        messages: The messages to preprocess

    Returns:
        The preprocessed messages
    """
    return messages


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
class ChatCompletion:
    """
    A wrapper for the OpenAI Chat API

    Attributes:
        use_case_name: name of the use case so it can be used as a collection name in MongoDB (e.g. "Q&A", "Quiz_Generation")
        config: A Config object
        model: The model to use for the chat completion
        model_params: A dictionary of parameters used to create the chat completion
        experiment_metadata: A dictionary of pre-defined metadata in project_experiment.ini about the experiment
        project_metadata: A dictionary of pre-defined metadata in project.ini about the project
        extra_params: Any extra parameters that should be stored in the MongoDB document
    """

    def __init__(self,
                 use_case_name: str,
                 config: Config,
                 model: str = "gpt-4",
                 model_params: Dict[str, Any] = None,
                 experiment_metadata: Dict[str, Any] = None,
                 project_metadata: Dict[str, Any] = None,
                 extra_params: Dict[Any, Any] = None):

        logging.info(f"Initializing ChatCompletion object for collection {use_case_name}")
        logging.info(f"ChatGPT Model: {model}")

        self.use_case_name = use_case_name
        self.config = config
        self.mongo_client = config.mongo_client
        self.async_mongo_client = config.async_mongo_client
        self.openai_client = config.openai_client

        self.model_params = {
            "model": model,
            "messages": [],
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 256,
            "stop": None,
            "user": "prosus-AI-team",
        }
        if model_params is None:
            logging.info(f"No model_params provided. Using default params: {self.model_params}")
        else:
            self.model_params.update(model_params)
            self.model_params["model"] = model
            logging.info(f"Updated default params. Updated params: {self.model_params}")

        self.experiment_metadata = experiment_metadata
        self.project_metadata = project_metadata
        self.extra_params = extra_params

    def create(self,
             messages: List[Dict[str, str]],
             functions: List[Dict[str, Union[str, Dict[str, Any]]]] = None,
             preprocess_messages: Callable = _preprocess_messages,
             process_response: Callable = _process_response,
             preprocess_messages_args: Dict[Any, Any] = None,
             process_response_args: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """
        Create a chat completion request and store it in MongoDB

        Args:
            messages: The messages to use for the chat completion
            functions: A list of functions to use for the chat completion
            preprocess_messages: A function that preprocesses the messages
            process_response: A function that processes the response
            preprocess_messages_args: A dictionary of arguments to pass to the preprocess_messages function
            process_response_args: A dictionary of arguments to pass to the process_response function

        Returns:
            A dictionary containing the chat completion request and response
        """

        if preprocess_messages_args is None:
            preprocess_messages_args = {}
        if process_response_args is None:
            process_response_args = {}

        preprocessed_messages = preprocess_messages(messages, **preprocess_messages_args)
        self.model_params["messages"] = preprocessed_messages

        if functions is not None:
            self.model_params["functions"] = functions

        response = self.openai_client.ChatCompletion.create(**self.model_params)

        if process_response is not None:
            response = process_response(response, **process_response_args)

        is_function_call = 'function_call' in response.choices[0].message

        document = {
            "messages": preprocessed_messages,
            "is_function_call": is_function_call,
            "response": response.choices[0].message["content"] if not is_function_call else None,
            "function_to_call": dict(response.choices[0].message["function_call"]) if is_function_call else None,
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