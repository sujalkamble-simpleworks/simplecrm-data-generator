"""utils/payloads.py
This module contains payloads used for API requests in the application."""

# pylint: disable=missing-function-docstring

from faker_utils import create_function


def access_token_payload(username:str, password:str):
    return {
        "grant_type": "password",
        "client_id": "741227e4-64d3-b2cd-0318-5f64953a436c",
        "client_secret": "ritesh",
        "username": "admin",
        "password": "gBGzvvVSoalc+v2bWZya6nJggBmRjXbhKRx/vXTpbBLUOJDqiFtjV8dKm7nfYuFcjyG9LNXc3oEe2C30S+5nN4RN5BOjPPIAHKPNIrBY7RRqEjqp4/ZGt44Uh2uSOQWI4jHlqnwztCXQ4qIa6jK2+dsm1WyRKWodRG5D2dI/7U8Pkmh/dz8dEV440aEto27ySwvM2d4C9Tc83zIGv+9OKLNocmLndeBNWojSc3NbDXI4TpLVnTGp77J8whutctGPFES6MoeuQRwGzVVI8xykHvUK7GGthoVXnGoYO8QGkxJncgNa5WIwxqP/CpIXFRkiZFev6mzfx5rNMuFBdw+umaoajREMOu971fjUr/QX7jdCm0Cxdqafoxf3Lgu5GkHAoEMzl0HJoYQ6Tm4vL8UN/FNAcUATDAFuLMyeUZyTW695AeAFn2mHV3jtLc0belZWsn4O/Cfb4rxqQtEV1bSlVesAV+ALzqFuz+pthvOj4bqUjPXJCTgZxypdyfrK3l6taJXXBuqJfq/ktYtGa7t8vmB3uyHuXNcARK3kXPo44bwc+jMiDOP86462YruhQ3pKxdj0uNnn7uRM3fiGXUNDDrft0/5B+NNMP/fMNCynDl2C6zQDQTx0Th60FvYuRwxCeboOdn5zM2N+uSei5YaDcm/WI6Co29ozcXMGfDy1+ZE=",
    }   


def create_record_payload(fields : list, module_name: str):
    """Generates a payload for creating a record in the specified module."""
    data = {
        "data": {
            "type": module_name,
            "attributes": {}
        }
    }

    for field in fields:
        field_name = field["name"]
        field_value = create_function(field)(None)
        data["data"]["attributes"][field_name] = field_value

    return data
