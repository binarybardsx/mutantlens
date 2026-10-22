from pydantic import BaseModel, ConfigDict


class Span(BaseModel):
    """Half-open range of character offsets into a source string."""

    model_config = ConfigDict(frozen=True)

    start: int
    end: int


class Mutant(BaseModel):
    """One small fault: replace `original` at `span` with `replacement`.

    `source_hash` ties the mutant to the exact source it was found in.
    """

    model_config = ConfigDict(frozen=True)

    operator: str
    span: Span
    original: str
    replacement: str
    source_hash: str
