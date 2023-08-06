import hashlib
from typing import Text, Union


def hash_md5(text: Union[Text, bytes]) -> Text:
    if isinstance(text, bytes):
        text_bytes = text
    elif isinstance(text, Text):
        text_bytes = text.encode()
    else:
        raise TypeError(f"Expected text or bytes, got {type(text)}")
    hash_object = hashlib.md5()
    hash_object.update(text_bytes)
    return hash_object.hexdigest()
