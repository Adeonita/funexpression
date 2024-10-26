from application.interfaces.expression_request_payload import Triplicate
import warnings
import functools


def get_srr_list(triplicate: Triplicate):
    return [
        triplicate.srr_acession_number_1,
        triplicate.srr_acession_number_2,
        triplicate.srr_acession_number_3,
    ]


def get_user_name_by_email(email: str):
    return email.split(".")[0]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func
