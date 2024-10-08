from typing import Any


class XmlParsingError(ValueError):
    def __init__(self, value: Any, expected_type: type):
        self.value = value
        self.expected_type = expected_type
        super().__init__(f"Cannot parse {value!r} as {expected_type}")


class InvalidElementCountError(ValueError):
    def __init__(self, expected: int, actual: int, section: type):
        self.expected = expected
        self.actual = actual
        super().__init__(f"Expected {expected} instance of {section}, got {actual}")


class SectionNotFoundError(ValueError):
    def __init__(self, section: type):
        super().__init__(f"Section {section} not found")


class InvalidSectionTypeError(TypeError):
    def __init__(self, expected_type: type, actual_type: type):
        super().__init__(f"Expected {expected_type}, got {expected_type}")
