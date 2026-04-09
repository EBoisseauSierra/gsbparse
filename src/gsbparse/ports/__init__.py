"""Ports — abstract interfaces declared by the domain.

This package is intentionally empty in the MVP.

A port is added the first time a second adapter implementation justifies the
abstraction.  The first anticipated port is ``BytesSource``, triggered when
encrypted-file reading support lands:

.. code-block:: python

    class BytesSource(Protocol):
        \"\"\"A source of .gsb file bytes.

        Implementations:
        - FileBytesSource(path)        — plain file on disk (default)
        - EncryptedBytesSource(path)   — decrypts a Grisbi-encrypted file
        - InMemoryBytesSource(data)    — useful in tests
        \"\"\"
        def read_bytes(self) -> bytes: ...

Until then, the XML adapter takes a ``pathlib.Path`` directly.
"""
