import random
import re
import string
from os import path
from uuid import uuid4


def _get_uuid(max_length=5):
    return str(uuid4()).replace("-", "")[:max_length]


def _get_random_string(length: int = 3):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def _slugify(s: str):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def generate_slug(s: str, with_suffix: bool = False):
    slug = _slugify(s)
    if with_suffix:
        slug = f"{slug}-{_get_random_string(3)}"
    return slug


def build_meta(obj):
    meta_str = "---\n"
    for attr in obj.meta_attrs:
        value = getattr(obj, attr)
        meta_str = meta_str + f"""{attr}: {value}\n"""
    meta_str = f"""{meta_str}---"""
    return meta_str


def camel_case(s):
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


S3_HOME_IDENTIFIER = "home/images"
S3_POST_IDENTIFIER = "post/images"
S3_SNIPPETS_IDENTIFIER = "snippet/images"
# S3_PROJECT_IDENTIFIER = "post/images"


def upload_to(filename, identifier=S3_POST_IDENTIFIER):
    file_split = path.splitext(filename)  # 0: filename, 1: ext
    _f_name = file_split[0]
    _f_ext = file_split[1]
    upload_file = f"{_slugify(_f_name)}-{_get_uuid(5)}"
    upload_path = f"{identifier}/{upload_file}{_f_ext}"
    return f"{upload_path}"
