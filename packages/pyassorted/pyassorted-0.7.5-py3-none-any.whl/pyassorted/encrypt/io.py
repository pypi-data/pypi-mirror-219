import base64
import hashlib
from typing import Optional, Text


def encode_file(raw_file_path: Text, encode_file_path: Text, password: Text) -> Text:
    """Encode a file with a password and save it to a new file."""

    with open(raw_file_path, "rb") as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        salt = b"__salt_of_password"
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        encoded_content = key + encoded_content

        with open(encode_file_path, "wb") as output_file:
            output_file.write(encoded_content)

    return encode_file_path


def decode_file(
    encode_file_path: Text, password: Text, decode_file_path: Optional[Text] = None
) -> bytes:
    """Decode a file with a password and save it to a new file."""

    with open(encode_file_path, "rb") as file:
        encoded_content = file.read()

        salt = b"__salt_of_password"
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

        if encoded_content[:32] == key:
            encoded_content = encoded_content[32:]
            decoded_content = base64.b64decode(encoded_content)

            if decode_file_path:
                with open(decode_file_path, "wb") as output_file:
                    output_file.write(decoded_content)
        else:
            raise ValueError("Wrong password")

    return decoded_content


class FileEncoder:
    def __init__(self, password: Text):
        self.__password = password

    def encode(self, raw_file_path: Text, encode_file_path: Text) -> Text:
        return encode_file(raw_file_path, encode_file_path, self.__password)

    def decode(
        self, encode_file_path: Text, decode_file_path: Optional[Text] = None
    ) -> bytes:
        return decode_file(encode_file_path, self.__password, decode_file_path)


if __name__ == "__main__":
    raw_file_path = "/tmp/test.txt"
    encode_file_path = "/tmp/test.txt.enc"
    content = "Hello World!"

    with open(raw_file_path, "w") as file:
        file.write(content)

    encode_file(raw_file_path, encode_file_path, "password")
    decode_content = decode_file(encode_file_path, "password")

    assert content == decode_content.decode()
