# Single source of truth for stdlib import statements.
# codegen.py imports STDLIB_IMPORTS and uses require_preamble() with these values.
# None means the function is handled inline in codegen (no top-level import needed).

STDLIB_IMPORTS: dict[str, str | None] = {
    # random number generation
    "random":     "import random",
    "xankhya":    "import random",
    # datetime
    "xomoy":      "from datetime import datetime",
    # file I/O — handled with a with-block in codegen; no preamble import needed
    "file_poha":  None,
    "file_likha": None,
    # HTTP
    "http_lua":   "import urllib.request",
}
