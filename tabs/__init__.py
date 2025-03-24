# This file makes the tabs directory a Python package
from .key_metrics import show_key_metrics_tab
from .user_device import show_user_device_tab
from .trip_characteristics import show_trip_characteristics_tab
from .predictive_model import show_predictive_model_tab
from .recommendations import show_recommendations_tab

__all__ = [
    'show_key_metrics_tab',
    'show_user_device_tab',
    'show_trip_characteristics_tab',
    'show_predictive_model_tab',
    'show_recommendations_tab'
]