from aplication.interfaces.expression_request_payload import Triplicate


def get_srr_list(triplicate: Triplicate):
    return [
        triplicate.srr_acession_number_1,
        triplicate.srr_acession_number_2,
        triplicate.srr_acession_number_3
    ]

def get_user_name_by_email(email:str):
    return email.split('.')[0]