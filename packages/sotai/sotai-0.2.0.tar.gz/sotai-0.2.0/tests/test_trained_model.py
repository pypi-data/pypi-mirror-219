"""Tests for Trained Model."""

import numpy as np
from sotai import TargetType, TrainedModel
from sotai.models import CalibratedLinear

from .utils import construct_trained_model


def test_trained_classification_model_predict(fixture_data, fixture_feature_configs):
    """Tests the predict function on a trained model."""
    trained_model = construct_trained_model(
        TargetType.CLASSIFICATION, fixture_data, fixture_feature_configs
    )
    predictions, probabilities = trained_model.predict(fixture_data)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(fixture_data)
    assert isinstance(probabilities, np.ndarray)
    assert len(probabilities) == len(fixture_data)


def test_trained_regression_model_predict(fixture_data, fixture_feature_configs):
    """Tests the predict function on a trained model."""
    trained_model = construct_trained_model(
        TargetType.REGRESSION, fixture_data, fixture_feature_configs
    )
    predictions, _ = trained_model.predict(fixture_data)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(fixture_data)


def test_trained_model_save_load(
    fixture_data,
    fixture_feature_configs,
    tmp_path,
):
    """Tests that a `TrainedModel` can be successfully saved and then loaded."""
    trained_model = construct_trained_model(
        TargetType.CLASSIFICATION, fixture_data, fixture_feature_configs
    )
    trained_model.save(tmp_path)
    loaded_trained_model = TrainedModel.load(tmp_path)
    assert isinstance(loaded_trained_model, TrainedModel)
    assert loaded_trained_model.dict(
        exclude={"model", "saved_filepath"}
    ) == trained_model.dict(exclude={"model", "saved_filepath"})
    assert isinstance(loaded_trained_model.model, CalibratedLinear)
