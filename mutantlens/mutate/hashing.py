import hashlib


def source_hash(source: str) -> str:
    """SHA-256 of the source text as UTF-8, in hex."""
    return hashlib.sha256(source.encode("utf-8")).hexdigest()
