import pytest
import tensorflow as tf

from app import model


def test_model_loaded():
    assert isinstance(model, tf.keras.Model)
