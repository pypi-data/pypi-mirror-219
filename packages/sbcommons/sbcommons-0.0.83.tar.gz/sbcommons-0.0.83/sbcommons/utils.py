import ast
import logging


def evaluate_recursively(obj, logger: logging.Logger = None):
    """ Evaluates a python object recursively.

        Example:
            "{'give_away': {'amount': 500}}"
            returns
            {give_away': {'amount': 500}}

        Args:
            obj: Any python object
            logger: Object for logging.

        Return:
            The actual evaluated python object down to the root element.
    """
    try:
        if isinstance(obj, list):
            data = [evaluate_recursively(el, logger) for el in obj]
        elif isinstance(obj, dict):
            data = obj
            for k, v in data.items():
                data[k] = evaluate_recursively(v, logger)
        elif isinstance(obj, tuple):
            data = (evaluate_recursively(el, logger) for el in obj)
        elif isinstance(obj, (int, bool, float)):
            return obj
        else:
            data = ast.literal_eval(obj)
            if isinstance(data, (list, dict, tuple)):
                data = evaluate_recursively(data)
        return data
    except (ValueError, SyntaxError) as e:
        # If we got a Value error try adding quotes to the object in case it is a string
        if isinstance(e, ValueError):
            try:
                data = ast.literal_eval("'" + obj + "'")
                return data
            except SyntaxError:
                pass
        # If adding quotes did not help then log a warning but return object as is
        if logger:
            logger.warning(f"Warning: object could not be parsed: {repr(e)}")
        return obj
