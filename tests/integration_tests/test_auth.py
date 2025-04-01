from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {"user_1": 1}
    jwt_token = AuthService().create_access_token(data=data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthService().decode_token(token=jwt_token)
    assert payload
    assert payload["user_1"] == data["user_1"]
