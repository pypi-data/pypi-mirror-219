"""A Pipeline for calibrated modeling."""
from __future__ import annotations

import logging
import os
import pickle
from time import sleep
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from .api import (
    get_api_key,
    get_inference_results,
    get_inference_status,
    post_inference,
    post_pipeline,
    post_pipeline_config,
    post_pipeline_feature_configs,
    post_trained_model,
    post_trained_model_analysis,
)
from .constants import INFERENCE_POLLING_INTERVAL, SOTAI_BASE_URL
from .data import determine_feature_types, replace_missing_values
from .enums import (
    APIStatus,
    FeatureType,
    InferenceConfigStatus,
    LossType,
    Metric,
    TargetType,
)
from .trained_model import TrainedModel
from .training import train_and_evaluate_model
from .types import (
    CategoricalFeatureConfig,
    Dataset,
    DatasetSplit,
    LinearConfig,
    NumericalFeatureConfig,
    PipelineConfig,
    PreparedData,
    TrainingConfig,
)


class Pipeline:  # pylint: disable=too-many-instance-attributes
    """A pipeline for calibrated modeling.

    The pipeline defines the configuration for training a calibrated model. The
    pipeline itself defines the features, target, and target type to be used. When
    training a model, the data and configuration used will be versioned and stored in
    the pipeline. The pipeline can be used to train multiple models with different
    configurations if desired; however, the target, target type, and primary metric
    should not be changed after initialization so that models trained by this pipeline
    can be compared.

    Example:

    ```python
    data = pd.read_csv(...)
    pipeline = Pipeline(features, target, TargetType.CLASSIFICATION)
    trained_model = pipeline.train(data)
    ```

    Attributes:
        ...
    """

    def __init__(
        self,
        features: List[str],
        target: str,
        target_type: TargetType,
        categories: Optional[Dict[str, Union[List[int], List[str]]]] = None,
        primary_metric: Optional[Metric] = None,
        name: Optional[str] = None,
    ):
        """Initializes an instance of `Pipeline`.

        The pipeline is initialized with a default config, which can be modified later.
        The target type can be optionally specfified. The default primary metric will be
        AUC for classification and Mean Squared Error for regression if not specified.

        Args:
            features: The column names in your data to use as features.
            target: The name of the target column.
            target_type: The type of the target column.
            categories: A dictionary mapping feature names to unique categories. Any
                values not in the categories list for a given feature will be treated
                as a missing value.
            primary_metric: The primary metric to use for training and evaluation.
            name: The name of the pipeline. If not provided, the name will be set to
                `{target}_{target_type}`.
        """
        self.name: str = name if name else f"{target}_{target_type}"
        self.target: str = target
        self.target_type: TargetType = target_type
        self.primary_metric: Metric = (
            primary_metric
            if primary_metric is not None
            else (
                Metric.AUC
                if self.target_type == TargetType.CLASSIFICATION
                else Metric.MSE
            )
        )
        self.feature_configs: Dict[
            str, Union[CategoricalFeatureConfig, NumericalFeatureConfig]
        ] = {
            feature_name: (
                CategoricalFeatureConfig(
                    name=feature_name,
                    categories=categories[feature_name],
                )
                if categories and feature_name in categories
                else NumericalFeatureConfig(name=feature_name)
            )
            for feature_name in features
        }
        self.shuffle_data: bool = True
        self.drop_empty_percentage: int = 70
        self.dataset_split: DatasetSplit = DatasetSplit(train=80, val=10, test=10)

        # Maps a pipeline config id to its corresponding `PipelineConfig`` instance.
        self.configs: Dict[int, PipelineConfig] = {}
        # Maps a dataset id to its corresponding `Dataset`` instance.
        self.datasets: Dict[int, Dataset] = {}

        # Tracks
        self.uuid = None
        self.trained_models: Dict[str, TrainedModel] = {}

    def prepare(  # pylint: disable=too-many-locals
        self,
        data: pd.DataFrame,
        pipeline_config_id: Optional[int] = None,
    ) -> Tuple[Dataset, PipelineConfig]:
        """Prepares the data and versions it along with the current pipeline config.

        If any features in data are detected as non-numeric, the pipeline will attempt
        to handle them as categorical features. Any features that the pipeline cannot
        handle will be skipped.

        Args:
            data: The raw data to be prepared for training.
            pipeline_config_id: The id of the pipeline config to be used for training.
                If not provided, the current pipeline config will be used and versioned.

        Returns:
            A tuple of the versioned dataset and pipeline config.
        """
        data.replace("", np.nan, inplace=True)  # treat empty strings as NaN
        if pipeline_config_id is None:
            pipeline_config_id = len(self.configs)
            pipeline_config = self._version_pipeline_config(data, pipeline_config_id)
            self.configs[pipeline_config_id] = pipeline_config
        else:
            pipeline_config = self.configs[pipeline_config_id]

        # Select only the features defined in the pipeline config.
        data = data[list(pipeline_config.feature_configs.keys()) + [self.target]]
        # Drop rows with too many missing values according to the drop empty percent.
        max_num_empty_columns = int(
            (pipeline_config.drop_empty_percentage * data.shape[1]) / 100
        )
        data = data[data.isnull().sum(axis=1) <= max_num_empty_columns]
        # Replace any missing values (i.e. NaN) with missing value constants.
        data = replace_missing_values(data, pipeline_config.feature_configs)
        if pipeline_config.shuffle_data:
            data = data.sample(frac=1).reset_index(drop=True)
        train_percentage = pipeline_config.dataset_split.train / 100
        train_data = data.iloc[: int(len(data) * train_percentage)]
        val_percentage = pipeline_config.dataset_split.val / 100
        val_data = data.iloc[
            int(len(data) * train_percentage) : int(
                len(data) * (train_percentage + val_percentage)
            )
        ]
        test_data = data.iloc[int(len(data) * (train_percentage + val_percentage)) :]

        dataset_id = len(self.datasets)
        dataset = Dataset(
            id=dataset_id,
            pipeline_config_id=pipeline_config_id,
            prepared_data=PreparedData(train=train_data, val=val_data, test=test_data),
        )
        self.datasets[dataset_id] = dataset

        return dataset, pipeline_config

    def train(
        self,
        data: Union[pd.DataFrame, int],
        pipeline_config_id: Optional[int] = None,
        model_config: Optional[LinearConfig] = None,
        training_config: Optional[TrainingConfig] = None,
    ) -> TrainedModel:
        """Returns a calibrated model trained according to the given configs.

        Args:
            data: The raw data to be prepared and trained on. If an int is provided,
                it is assumed to be a dataset id and the corresponding dataset will be
                used.
            pipeline_config_id: The id of the pipeline config to be used for training.
                If not provided, the current pipeline config will be versioned and used.
                If data is an int, this argument is ignored and the pipeline config used
                to prepare the data with the given id will be used.
            model_config: The config to be used for training the model. If not provided,
                a default config will be used.
            training_config: The config to be used for training the model. If not
                provided, a default config will be used.

        Returns:
            A `TrainedModel` instance.
        """
        if isinstance(data, int):
            dataset = self.datasets[data]
            pipeline_config = self.configs[dataset.pipeline_config_id]
        else:
            dataset, pipeline_config = self.prepare(data, pipeline_config_id)

        if model_config is None:
            model_config = LinearConfig()

        if training_config is None:
            training_config = TrainingConfig(
                loss_type=LossType.BINARY_CROSSENTROPY
                if self.target_type == TargetType.CLASSIFICATION
                else LossType.MSE
            )

        model, training_results = train_and_evaluate_model(
            dataset,
            self.target,
            self.primary_metric,
            pipeline_config,
            model_config,
            training_config,
        )

        return TrainedModel(
            dataset_id=dataset.id,
            pipeline_config=pipeline_config,
            model_config=model_config,
            training_config=training_config,
            training_results=training_results,
            model=model,
        )

    def publish(self) -> Optional[str]:
        """Uploads the pipeline to the SOTAI web client.

        Returns:
            If the pipeline was successfully uploaded, the pipeline UUID.
            Otherwise, None.
        """
        pipeline_response_status, pipeline_uuid = post_pipeline(self)
        if pipeline_response_status == APIStatus.ERROR:
            return None

        self.uuid = pipeline_uuid
        return self.uuid

    def analysis(  # pylint: disable=too-many-return-statements
        self,
        trained_model: TrainedModel,
    ) -> Optional[str]:
        """Charts the results for the specified trained model in the SOTAI web client.

        This function requires an internet connection and a SOTAI account. The trained
        model will be uploaded to the SOTAI web client for analysis.

        If you would like to analyze the results for a trained model without uploading
        it to the SOTAI web client, the data is available in `training_results`.

        Args:
            trained_model: The trained model to be analyzed.

        Returns:
            If the analysis was successfully run, the analysis URL. Otherwise `None`.
        """
        if trained_model.analysis_url:  # early exit if analysis has already been run.
            return trained_model.analysis_url

        if not get_api_key():
            raise ValueError(
                "You must have an API key to run analysis."
                " Please visit app.sotai.ai to get an API key."
            )

        if self.uuid is None:
            self.uuid = self.publish()

        if self.uuid is None:
            return None

        pipeline_config_response_status, pipeline_config_uuid = post_pipeline_config(
            self.uuid, trained_model.pipeline_config
        )

        if pipeline_config_response_status == APIStatus.ERROR:
            return None

        trained_model.pipeline_config.uuid = pipeline_config_uuid

        feature_config_response_status = post_pipeline_feature_configs(
            pipeline_config_uuid, trained_model.pipeline_config.feature_configs
        )

        if feature_config_response_status == APIStatus.ERROR:
            return None

        analysis_response_status, analysis_results = post_trained_model_analysis(
            pipeline_config_uuid, trained_model
        )

        if analysis_response_status == APIStatus.ERROR:
            return None

        trained_model.uuid = analysis_results["trainedModelMetadataUUID"]

        upload_response = self._upload_model(trained_model)
        if upload_response == APIStatus.ERROR:
            return None

        # TODO: update to use response analysisUrl once no longer broken.
        analysis_url = (
            f"{SOTAI_BASE_URL}/pipelines/{self.uuid}"
            f"/trained-models/{trained_model.uuid}"
        )
        trained_model.analysis_url = analysis_url

        return analysis_url

    def inference(
        self,
        filepath: str,
        trained_model_uuid: str,
    ) -> Optional[str]:
        """Runs inference on a dataset with a trained model in the SOTAI cloud.

        Args:
            inference_dataset_path: The path to the dataset to run inference on.
            trained_model: The trained model to use for inference.

        Returns:
            If UUID of the inference run. If unsuccessful, `None`.
        """

        if not get_api_key():
            raise ValueError(
                "You must have an API key to run inference."
                " Please visit app.sotai.ai to get an API key."
            )
        inference_response_status, inference_uuid = post_inference(
            filepath, trained_model_uuid
        )
        if inference_response_status == APIStatus.ERROR:
            return None

        return inference_uuid

    def await_inference(
        self,
        inference_uuid: str,
        inference_results_folder_path: str,
    ):
        """Polls the SOTAI cloud for the results of the specified inference job.

        Args:
            inference_uuid: The uuid of the inference job to poll.
            inference_results_folder_path: The path to save the inference results to.

        Returns:
            If inference was successfully run, the path to the inference results.
        """
        while True:
            inference_response_status, inference_job_status = get_inference_status(
                inference_uuid
            )
            logging.info("Current inference job status: %s", inference_job_status)
            if (
                inference_response_status == APIStatus.SUCCESS
                and inference_job_status == InferenceConfigStatus.SUCCESS
            ):
                get_inference_response = get_inference_results(
                    inference_uuid, inference_results_folder_path
                )
                if get_inference_response == APIStatus.ERROR:
                    logging.info("Error getting inference results")
                else:
                    logging.info(
                        "Inference results saved to: %s ", inference_results_folder_path
                    )
                return inference_results_folder_path

            sleep(INFERENCE_POLLING_INTERVAL)

    def save(self, filepath: str):
        """Saves the pipeline to the specified filepath.

        Args:
            filepath: The directory to which the pipeline wil be saved. If the directory
                does not exist, this function will attempt to create it. If the
                directory already exists, this function will overwrite any existing
                content with conflicting filenames.
        """
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(os.path.join(filepath, "pipeline.pkl"), "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath: str) -> Pipeline:
        """Loads the pipeline from the specified filepath.

        Args:
            filepath: The filepath from which to load the pipeline. The filepath should
                point to a file created by the `save` method of a `TrainedModel`
                instance.

        Returns:
            A `Pipeline` instance.
        """
        with open(os.path.join(filepath, "pipeline.pkl"), "rb") as file:
            pipeline = pickle.load(file)

        return pipeline

    @classmethod
    def from_config(
        cls, config: PipelineConfig, name: Optional[str] = None
    ) -> Pipeline:
        """Returns a new pipeline created from the specified config."""
        pipeline = cls(
            features=list(config.feature_configs.keys()),
            target=config.target,
            target_type=config.target_type,
            primary_metric=config.primary_metric,
            name=name,
        )
        pipeline.feature_configs = config.feature_configs
        pipeline.shuffle_data = config.shuffle_data
        pipeline.drop_empty_percentage = config.drop_empty_percentage
        pipeline.dataset_split = config.dataset_split

        return pipeline

    ############################################################################
    #                            Private Methods                               #
    ############################################################################

    def _version_pipeline_config(self, data: pd.DataFrame, pipeline_config_id: int):
        """Returns a new `PipelineConfig` instance verisoned from the current config."""
        pipeline_config = PipelineConfig(
            id=pipeline_config_id,
            target=self.target,
            target_type=self.target_type,
            primary_metric=self.primary_metric,
            feature_configs=self.feature_configs,
            shuffle_data=self.shuffle_data,
            drop_empty_percentage=self.drop_empty_percentage,
            dataset_split=self.dataset_split,
        )

        feature_types = determine_feature_types(
            data[list(pipeline_config.feature_configs.keys())]
        )
        for feature_name, feature_type in feature_types.items():
            feature_config = pipeline_config.feature_configs[feature_name]
            if (
                feature_type == FeatureType.NUMERICAL
                or feature_config.type == FeatureType.CATEGORICAL
            ):
                continue
            if feature_type == FeatureType.CATEGORICAL:
                logging.info(
                    "Detected %s as categorical. Replacing numerical config with "
                    "default categorical config using unique values as categories",
                    feature_name,
                )
                pipeline_config.feature_configs[
                    feature_name
                ] = CategoricalFeatureConfig(
                    name=feature_name,
                    categories=sorted(data[feature_name].dropna().unique().tolist()),
                )
            else:
                logging.info(
                    "Removing feature %s because its data type is not supported.",
                    feature_name,
                )
                pipeline_config.feature_configs.pop(feature_name)

        return pipeline_config

    def _upload_model(
        self,
        trained_model: TrainedModel,
    ) -> APIStatus:
        """Uploads the trained model to the SOTAI web client.

        If a model has already been uploaded, this function will return without
        uploading the model again. This function requires an internet connection and a
        SOTAI account. The trained model will be uploaded to the SOTAI web client for
        inference.

        Args:
            trained_model: The trained model to upload.
        """

        if not get_api_key():
            raise ValueError(
                "You must have an API key to upload a model."
                " Please visit app.sotai.ai to get an API key."
            )
        model_save_folder_path = f"/tmp/sotai/model/{trained_model.uuid}"

        if trained_model.uuid is None:
            raise ValueError("Must run analysis to generate uuid before uploading.")

        trained_model.save(model_save_folder_path)
        trained_model_response = post_trained_model(
            model_save_folder_path, trained_model.uuid
        )
        self.trained_models[trained_model.uuid] = trained_model
        return trained_model_response
