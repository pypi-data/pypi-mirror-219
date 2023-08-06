# Use the functions below to get the desired model for training.
from typing import Dict, NoReturn

from transformers import AutoConfig, AutoModelForTokenClassification


class ModelPicker(object):
    """
    This class is used to pick the model we are using to train.
    The class provides functions that returns the desired model objects
    i.e get the desired model for training etc
    """

    def __init__(
            self,
            model_name_or_path: str,
            config: AutoConfig,
            cache_dir: str,
            model_revision: str,
            use_auth_token: bool
    ) -> NoReturn:
        """
        Initialize the variables needed for loading the huggingface models
        Args:
            model_name_or_path (str): Path to pretrained model or model identifier from huggingface.co/models
            config (AutoConfig): Pretrained config object
            cache_dir (str): Where do you want to store the pretrained models downloaded from huggingface.co
            model_revision (str): The specific model version to use (can be a branch name, tag name or commit id).
            use_auth_token (bool): Will use the token generated when running `transformers-cli login` 
                                   (necessary to use this script with private models).
        """
        self._model_name_or_path = model_name_or_path
        self._config = config
        self._cache_dir = cache_dir
        self._model_revision = model_revision
        self._use_auth_token = use_auth_token

    def get_argmax_bert_model(self) -> AutoModelForTokenClassification:
        """
        Return a model that uses argmax to process the model logits for obtaining the predictions
        and calculating the loss
        Returns:
            (AutoModelForTokenClassification): Return argmax token classification model
        """
        return AutoModelForTokenClassification.from_pretrained(
            self._model_name_or_path,
            from_tf=bool(".ckpt" in self._model_name_or_path),
            config=self._config,
            cache_dir=self._cache_dir,
            revision=self._model_revision,
            use_auth_token=self._use_auth_token,
        )
