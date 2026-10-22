from mutantlens.contracts.mutant import Mutant
from mutantlens.mutate.hashing import source_hash


class StaleMutantError(Exception):
    """The mutant was found in different source than the source given to apply."""


def apply(source: str, mutant: Mutant) -> str:
    """Return `source` with `mutant` applied. Pure: never touches the filesystem.

    Raises StaleMutantError if `source` is not the source the mutant was found in.
    """
    actual = source_hash(source)
    if actual != mutant.source_hash:
        raise StaleMutantError(
            f"mutant was found in source with hash {mutant.source_hash[:12]}, "
            f"but the source given has hash {actual[:12]}"
        )
    return source[: mutant.span.start] + mutant.replacement + source[mutant.span.end :]
