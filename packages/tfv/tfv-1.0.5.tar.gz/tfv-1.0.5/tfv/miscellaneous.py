import numpy as np
import pandas as pd

# ToDO:
class Expression:
    @classmethod
    def decorator(cls, function_call):
        def wrapper(*args, **kwargs):
            base = args[0]
            variables = args[1]  # variable(s) should always be first required argument

            post_process = kwargs.pop("post_process", None)

            # Special case for Current speed / Direction. Patched to first check if they are present (tfv.xarray)
            if (
                (variables == "V")
                & (post_process is None)
                & ("V" not in base.variables)
            ):
                variables = ["V_x", "V_y"]
                post_process = lambda x: np.hypot(*x)

            elif (
                (variables == "VDir")
                & (post_process is None)
                & ("VDir" not in base.variables)
            ):
                variables = ["V_y", "V_x"]
                post_process = lambda x: (90 - np.arctan2(*x) * 180 / np.pi) % 360

            if type(variables) == str:
                output = function_call(*args, **kwargs)
            elif type(variables) == list:
                data = []
                for v in variables:
                    arr = function_call(base, v, *args[2:], **kwargs)
                    data.append(arr)
                output = np.ma.stack(data)

            if post_process:
                output = post_process(output.astype(float))

            return output

        return wrapper


def unsupported_decorator(function_call):
    def wrapper(*args):
        name = function_call.__name__
        message = "{} is currently not supported".format(name)
        print(message)

    return wrapper
