"""convert files to csv"""
from typing import Literal, TypedDict

CsvOptions = TypedDict(
    "CsvOptions", {"delimiter": str, "quoting": Literal[1], "quotechar": str}
)
