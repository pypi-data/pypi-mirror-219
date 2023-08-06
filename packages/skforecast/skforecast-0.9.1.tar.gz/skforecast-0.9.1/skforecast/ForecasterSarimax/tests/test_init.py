# Unit test __init__ ForecasterSarimax
# ==============================================================================
import re
import pytest
from pytest import approx
import numpy as np
import pandas as pd
from skforecast.ForecasterSarimax import ForecasterSarimax
from pmdarima.arima import ARIMA
from sklearn.linear_model import LinearRegression


def test_TypeError_when_regressor_is_not_pmdarima_ARIMA_when_initialization():
    """
    Raise TypeError if regressor is not of type pmdarima.arima.ARIMA when initializing the forecaster.
    """
    regressor = LinearRegression()

    err_msg = re.escape(
                (f"`regressor` must be an instance of type pmdarima.arima.ARIMA. "
                 f"Got {type(regressor)}.")
            ) 
    with pytest.raises(TypeError, match = err_msg):
        ForecasterSarimax(regressor = regressor)


def test_pmdarima_ARIMA_params_are_stored_when_initialization():
    """
    Check `params` are stored in the forecaster.
    """
    forecaster = ForecasterSarimax(regressor = ARIMA(order=(1,1,1)))
    expected_params = ARIMA(order=(1,1,1)).get_params(deep=True)

    assert forecaster.params == expected_params