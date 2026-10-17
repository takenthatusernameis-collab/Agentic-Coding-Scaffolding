import io

import plistlib_utils


def test_roundtrip_bytes():
    obj = {"a": 1, "b": [2, 3]}
    data = plistlib_utils.plist_dumps(obj)
    assert plistlib_utils.plist_loads(data) == obj


def test_load_dump_file():
    obj = {"x": "y"}
    buf = io.BytesIO()
    plistlib_utils.plist_dump(obj, buf)
    buf.seek(0)
    assert plistlib_utils.plist_load(buf) == obj
