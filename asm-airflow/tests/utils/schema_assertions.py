from typing import Any


def assert_shape(actual: Any, expected: Any, path="root"):
    """
    Recursively assert that actual matches the expected shape.
    Values are ignored; only structure & types matter.
    """

    # --- UNION TYPE ---
    if isinstance(expected, dict) and "anyOf" in expected:
        allowed = expected["anyOf"]

        type_map = {
            "number": (int, float),
            "string": str,
            "null": type(None),
            "object": dict,
            "array": list,
            "boolean": bool,
        }

        assert any(
            isinstance(actual, type_map[t]) for t in allowed
        ), f"{path} should be one of {allowed}, got {type(actual)}"
        return
    # --- PRIMITIVE TYPE ---
    if isinstance(expected, str):
        type_map = {
            "number": (int, float),
            "string": str,
            "null": type(None),
            "object": dict,
            "array": list,
            "boolean": bool,
        }

        assert isinstance(actual, type_map[expected]), (
            f"{path} should be {expected}, got {type(actual)}"
        )
        return


    # --- OBJECT ---
    if isinstance(expected, dict):
        assert isinstance(actual, dict), f"{path} should be dict"
        for key, sub in expected.items():
            assert key in actual, f"Missing key: {path}.{key}"
            assert_shape(actual[key], sub, f"{path}.{key}")
        return

    # --- ARRAY ---
    elif isinstance(expected, list):
        type_map = {
            "number": (int, float),
            "string": str,
            "null": type(None),
            "object": dict,
            "array": list,
            "boolean": bool,
        }

        # UNION shorthand: ["string", "null"]
        if expected and all(isinstance(x, str) for x in expected):
            assert any(
                isinstance(actual, type_map[t]) for t in expected
            ), f"{path} should be one of {expected}, got {type(actual)}"
            return

    # ARRAY schema: [ {...} ]
    assert isinstance(actual, list), f"{path} should be list"
    if expected:
        for i, item in enumerate(actual):
            assert_shape(item, expected[0], f"{path}[{i}]")

    else:
        type_map = {
            "number": (int, float),
            "string": str,
            "null": type(None),
            "object": dict,
            "array": list,
            "boolean": bool,
        }

        assert isinstance(
            actual, type_map[expected]
        ), f"{path} should be {expected}"
