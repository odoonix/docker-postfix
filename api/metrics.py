
import prometheus_client
import time as times
import functools


mitrics_map = {}


def _metric_gauge(func_name, *args_metric):
    # Create metrics if not exist
    for metric in args_metric:
        if metric not in mitrics_map:
            mitrics_map[metric] = prometheus_client.Gauge(metric, "")

    # Creates a wraper
    def wrapper(original_function):
        @functools.wraps(original_function)
        def new_function(*args, **kwargs):
            for metric in args_metric:
                func = getattr(mitrics_map[metric], func_name)
                func()
            return original_function(*args, **kwargs)
        return new_function
    return wrapper


def inc(*args_metric):
    return _metric_gauge('inc', *args_metric)


def dec(*args_metric):
    return _metric_gauge('dec', *args_metric)


def time(*args_metric):
    # Create metrics if not exist
    for metric in args_metric:
        if metric not in mitrics_map:
            mitrics_map[metric] = prometheus_client.Summary(metric, "")


    # Creates a wraper
    def wrapper(original_function):
        start_time = times.time()
        @functools.wraps(original_function)
        def new_function(*args, **kwargs):
            for metric in args_metric:
                mitrics_map[metric].observe(times.time() - start_time)
            return original_function()
        return new_function
    return wrapper


def generate_latest():
    return prometheus_client.generate_latest()
