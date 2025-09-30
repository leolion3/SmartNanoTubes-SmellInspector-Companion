from typing import List, Dict, Any

import numpy as np


def _compute_average_ambient_humidity(
        humidity_list: List[str],
        avg_bias: float = 1
) -> float:
    """
    Computes the average air humidity to re-label falsely labelled substances back to "air".
    :param avg_bias: bias to scale up the humidity to filter out more data. Default: 1.25 (125%).
    :return: the average air humidity of the experiment.
    """
    average_humidity = sum([float(x) for x in humidity_list]) / len(humidity_list)
    return average_humidity * avg_bias


def _re_label_windowed_data(
        data: List[Dict[str, Any]],
        humidity_list: List[str],
        classification_start_idx: int,
        classification_end_idx: int
) -> None:
    average_ambient_humidity = _compute_average_ambient_humidity(humidity_list)
    window_humidities = [
        float(data[i]['humidity'])
        for i in range(classification_start_idx, classification_end_idx + 1)
    ]

    # compute the 75th percentile (upper 25%)
    upper_25th = float(np.percentile(window_humidities, 10))
    threshold = (average_ambient_humidity + upper_25th) / 2.0

    # re-label points where humidity <= threshold
    for i in range(classification_start_idx, classification_end_idx + 1):
        if float(data[i]['humidity']) <= threshold:
            data[i]['label'] = 'air'


def re_label_data(data: List[Dict[str, Any]]) -> None:
    window_frame = []
    i = -1
    while i < len(data) - 1:
        i += 1
        dp = data[i]
        if dp['label'] == 'air':
            window_frame.append(dp['humidity'])
            continue
        classification_start = i
        while i < len(data) and data[i]['label'] != 'air':
            i += 1
        classification_end = i - 1
        _re_label_windowed_data(data, window_frame, classification_start, classification_end)
        window_frame = []
