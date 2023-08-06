"""This module contains the API functions for interacting with the SOTAI API.""" ""
import logging
import os
import tarfile
import urllib
from typing import Dict, Optional, Tuple, Union

import requests

from .constants import SOTAI_API_ENDPOINT, SOTAI_API_TIMEOUT, SOTAI_BASE_URL
from .enums import APIStatus, InferenceConfigStatus
from .trained_model import TrainedModel
from .types import (
    CategoricalFeatureConfig,
    FeatureType,
    NumericalFeatureConfig,
    PipelineConfig,
)


def set_api_key(api_key: str):
    """Set the SOTAI API key in the environment variables.

    Args:
        api_key: The API key to set.
    """
    os.environ["SOTAI_API_KEY"] = api_key


def get_api_key() -> str:
    """Returns the SOTAI API key from the environment variables."""
    return os.environ["SOTAI_API_KEY"]


def get_auth_headers() -> Dict[str, str]:
    """Returns the authentication headers for a pipeline."""
    return {
        "sotai-api-key": get_api_key(),
    }


def post_pipeline(pipeline) -> Tuple[APIStatus, Optional[str]]:
    """Create a new pipeline on the SOTAI API.

    Args:
        pipeline: The pipeline to create.

    Returns:
        A tuple containing the status of the API call and the UUID of the created
        pipeline. If unsuccessful, the UUID will be `None`.
    """
    response = requests.post(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/pipelines",
        json={
            "name": pipeline.name,
            "target": pipeline.target,
            "target_column_type": pipeline.target_type,
            "primary_metric": pipeline.primary_metric,
        },
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )
    if response.status_code != 200:
        logging.error("Failed to create pipeline")
        return APIStatus.ERROR, None

    return APIStatus.SUCCESS, response.json()["uuid"]


def post_pipeline_config(
    pipeline_uuid: str, pipeline_config: PipelineConfig
) -> Tuple[APIStatus, Optional[str]]:
    """Create a new pipeline config on the SOTAI API.

    Args:
        pipeline_uuid: The pipeline uuid to create the pipeline config for.
        pipeline_config : The pipeline config to create.

    Returns:
        A tuple containing the status of the API call and the UUID of the created
        pipeline. If unsuccessful, the UUID will be `None`.
    """
    response = requests.post(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/pipelines/{pipeline_uuid}/pipeline-configs",
        json={
            "shuffle_data": pipeline_config.shuffle_data,
            "drop_empty_percentage": pipeline_config.drop_empty_percentage,
            "train_percentage": pipeline_config.dataset_split.train,
            "validation_percentage": pipeline_config.dataset_split.val,
            "test_percentage": pipeline_config.dataset_split.test,
        },
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )

    if response.status_code != 200:
        logging.error("Failed to create pipeline config")
        return APIStatus.ERROR, None

    return APIStatus.SUCCESS, response.json()["uuid"]


def post_pipeline_feature_configs(
    pipeline_config_uuid: str,
    feature_configs: Dict[str, Union[CategoricalFeatureConfig, NumericalFeatureConfig]],
) -> APIStatus:
    """Create a new pipeline feature configs on the SOTAI API.

    Args:
        pipeline_config_uuid: The pipeline config uuid to create the pipeline
            feature configs for.
        feature_configs: The feature configs to create.

    Returns:
        The status of the API call.
    """
    sotai_feature_configs = []

    for feature_config in feature_configs.values():
        sotai_feature_config = {
            "feature_name": feature_config.name,
            "feature_type": feature_config.type,
        }
        if feature_config.type == FeatureType.CATEGORICAL:
            if isinstance(feature_config.categories[0], int):
                sotai_feature_config["categories_int"] = feature_config.categories
            else:
                sotai_feature_config["categories_str"] = feature_config.categories
        else:
            sotai_feature_config["num_keypoints"] = feature_config.num_keypoints
            sotai_feature_config[
                "input_keypoints_init"
            ] = feature_config.input_keypoints_init
            sotai_feature_config[
                "input_keypoints_type"
            ] = feature_config.input_keypoints_type
            sotai_feature_config["monotonicity"] = feature_config.monotonicity

        sotai_feature_configs.append(sotai_feature_config)

    response = requests.post(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/pipeline-configs/"
        f"{pipeline_config_uuid}/feature-configs",
        json=sotai_feature_configs,
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )

    if response.status_code != 200:
        logging.error("Failed to create pipeline feature configs")
        return APIStatus.ERROR

    return APIStatus.SUCCESS


def post_trained_model_analysis(
    pipeline_config_uuid: str, trained_model: TrainedModel
) -> Tuple[APIStatus, Optional[Dict[str, str]]]:
    """Create a new trained model analysis on the SOTAI API.

    Args:
        pipeline_config_uuid: The pipeline config uuid to create the trained model
            analysis for.
        trained_model: The trained model to create.

    Returns:
        A tuple containing the status of the API call and a dict containing the UUIDs
        of the resources created as well as a link that can be used to view the trained
        model analysis. If unsuccessful, the UUID will be `None`.

        Keys:
            - `trainedModelMetadataUUID`: The UUID of the trained model.
            - `modelConfigUUID`: The UUID of the model configuration.
            - `pipelineConfigUUID`: The UUID of the pipeline configuration.
            - `analysisURL`: The URL of the trained model analysis.
    """
    training_results = trained_model.training_results
    train_primary_metrics = training_results.train_primary_metric_by_epoch
    val_primary_metrics = training_results.val_primary_metric_by_epoch
    overall_model_results_dict = {
        "epochs": trained_model.training_config.epochs,
        "batch_size": trained_model.training_config.batch_size,
        "learning_rate": trained_model.training_config.learning_rate,
        "runtime_in_seconds": training_results.training_time,
        "train_loss_per_epoch": training_results.train_loss_by_epoch,
        "train_primary_metric_per_epoch": train_primary_metrics,
        "validation_loss_per_epoch": training_results.val_loss_by_epoch,
        "validation_primary_metric_per_epoch": val_primary_metrics,
        "test_loss": training_results.test_loss,
        "test_primary_metric": training_results.test_primary_metric,
        "feature_names": [
            feature.feature_name for feature in trained_model.model.features
        ],
        "linear_coefficients": [
            training_results.linear_coefficients[feature.feature_name]
            for feature in trained_model.model.features
        ],
    }
    feature_analyses_list = [
        {
            "feature_name": feature.feature_name,
            "feature_type": feature.feature_type.value,
            "statistic_min": feature.min,
            "statistic_max": feature.max,
            "statistic_mean": feature.mean,
            "statistic_median": feature.median,
            "statistic_std": feature.std,
            "keypoints_outputs": feature.keypoints_outputs,
            "keypoints_inputs_categorical": feature.keypoints_inputs_categorical,
            "keypoints_inputs_numerical": feature.keypoints_inputs_numerical,
        }
        for feature in trained_model.training_results.feature_analyses.values()
    ]
    trained_model_metadata_dict = {
        "epochs": trained_model.training_config.epochs,
        "batch_size": trained_model.training_config.batch_size,
        "learning_rate": trained_model.training_config.learning_rate,
        "train_primary_metric": [training_results.train_primary_metric_by_epoch[-1]],
        "validation_primary_metric": [training_results.val_primary_metric_by_epoch[-1]],
        "test_primary_metric": training_results.test_primary_metric,
    }

    model_config_dict = {
        "model_framework": "pytorch",
        "model_type": "linear",
        "loss_type": trained_model.training_config.loss_type.value,
        "primary_metric": trained_model.pipeline_config.primary_metric.value,
        "target_column_type": trained_model.pipeline_config.target_type.value,
        "target_column": trained_model.pipeline_config.target,
        "model_config_name": "Model 1",
    }

    response = requests.post(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/pipeline-configs/{pipeline_config_uuid}/analysis",
        json={
            "trained_model_metadata": trained_model_metadata_dict,
            "overall_model_results": overall_model_results_dict,
            "model_config": model_config_dict,
            "feature_analyses": feature_analyses_list,
        },
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )

    if response.status_code != 200:
        logging.error("Failed to create trained model analysis")
        return APIStatus.ERROR, None

    return APIStatus.SUCCESS, response.json()


def post_trained_model(trained_model_path: str, trained_model_uuid: str) -> APIStatus:
    """Create a new trained model on the SOTAI API.

    Args:
        trained_model_path: The path to the trained model file to post.
        trained_model_uuid: The UUID of the trained model.

    Returns:
        The status of the API call.
    """
    original_filepath = f"{trained_model_path}/trained_ptcm_model.pt"
    tar_filepath = f"{trained_model_path}/model.tar.gz"
    with tarfile.open(tar_filepath, "w:gz") as tar:
        tar.add(original_filepath, arcname="model.pt")

    with open(tar_filepath, "rb") as data_file:
        response = requests.post(
            f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/models",
            files={"file": data_file},
            data={"trained_model_metadata_uuid": trained_model_uuid},
            headers=get_auth_headers(),
            timeout=SOTAI_API_TIMEOUT,
        )

    if response.status_code != 200:
        logging.error("Failed to create trained model")
        return APIStatus.ERROR

    return APIStatus.SUCCESS


def post_inference(
    data_filepath: str,
    trained_model_uuid: str,
) -> Tuple[APIStatus, Optional[str]]:
    """Create a new inference on the SOTAI API .

    Args:
        data_filepath: The path to the data file to create the inference for.
        trained_model_uuid: The trained model uuid to create the inference for.

    Returns:
        A tuple containing the status of the API call and the UUID of the created
        inference job. If unsuccessful, the UUID will be None.
    """
    with open(data_filepath, "rb") as data_file:
        response = requests.post(
            f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/inferences",
            files={"file": data_file},
            data={"trained_model_metadata_uuid": trained_model_uuid},
            headers=get_auth_headers(),
            timeout=SOTAI_API_TIMEOUT,
        )

    if response.status_code != 200:
        logging.error("Failed to create inference")
        return APIStatus.ERROR, None

    return APIStatus.SUCCESS, response.json()["inferenceConfigUUID"]


def get_inference_status(
    inference_uuid: str,
) -> Tuple[APIStatus, Optional[InferenceConfigStatus]]:
    """Get an inference from the SOTAI API.

    Args:
        inference_uuid: The UUID of the inference to get.

    Returns:
       A tuple containing the status of the API call and the status of the inference job
       if the API call is successful. If unsuccessful, the UUID will be `None`.
    """
    response = requests.get(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/inferences/{inference_uuid}/status",
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )

    if response.status_code != 200:
        logging.error("Failed to get inference")
        return APIStatus.ERROR, None

    return APIStatus.SUCCESS, response.json()


def get_inference_results(inference_uuid: str, download_folder: str) -> APIStatus:
    """Get an inference from the SOTAI API.

    Args:
        inference_uuid: The UUID of the inference results to get.

    Returns:
        The status of the API call.
    """
    response = requests.get(
        f"{SOTAI_BASE_URL}/{SOTAI_API_ENDPOINT}/inferences/{inference_uuid}/download",
        headers=get_auth_headers(),
        timeout=SOTAI_API_TIMEOUT,
    )

    if response.status_code != 200:
        print("Failed to get inference")
        logging.error("Failed to get inference")
        return APIStatus.ERROR

    urllib.request.urlretrieve(
        response.json(), f"{download_folder}/inference_results.csv"
    )

    return APIStatus.SUCCESS
