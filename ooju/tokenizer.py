import re
from dataclasses import dataclass
from enum import Enum, auto


class TT(Enum):
    # literals
    NUMBER      = auto()
    STRING      = auto()
    BOOL        = auto()
    NONE        = auto()

    # identifiers & keywords
    KEYWORD     = auto()
    IDENT       = auto()

    # operators
    ASSIGN      = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN= auto()
    STAR_ASSIGN = auto()
    SLASH_ASSIGN= auto()
    PLUS        = auto()
    MINUS       = auto()
    STAR        = auto()
    SLASH       = auto()
    PERCENT     = auto()
    EQ          = auto()
    NEQ         = auto()
    LT          = auto()
    GT          = auto()
    LTE         = auto()
    GTE         = auto()
    AND         = auto()
    OR          = auto()
    NOT         = auto()
    DOT         = auto()

    # delimiters
    LPAREN      = auto()
    RPAREN      = auto()
    LBRACKET    = auto()
    RBRACKET    = auto()
    LBRACE      = auto()
    RBRACE      = auto()
    COMMA       = auto()
    COLON       = auto()
    NEWLINE     = auto()
    INDENT      = auto()
    DEDENT      = auto()
    EOF         = auto()

    # passthrough
    RAW         = auto()


ASSAMESE_TO_ROMANIZED_KEYWORDS = {
    "ধৰা": "dhora",
    "কোৱা": "kua",
    "লোৱা": "lua",
    "কাম": "kaam",
    "যদি": "jodi",
    "নহলে": "nohole",
    "বা": "ba",
    "তেতিয়া": "tetia",
    "বাৰে": "bare",
    "কৰা": "kora",
    "যেতিয়ালৈকে": "jetialoike",
    "বাৰ": "bar",
    "সমাপ্ত": "homapto",
    
    "লগ_কৰা": "log_kora",
    "ডেল_কৰা": "del_kora",
    "লেন_জোখা": "len_jukha",
    "চৰ্ট": "sort",
    "আছে": "ase",
    "ত": "t",
    
    "ওপৰ": "upor",
    "তল": "tol",
    "কটা": "kata",
    "গুচোৱা": "gusua",
    "Lগুচোৱা": "Lgusua",
    "Rগুচোৱা": "Rgusua",
    "বিচৰা": "bisara",
    "নিদিয়া": "nidiya",
    "দীঘল": "dighol",
    
    "মজিয়া": "mojiya",
    "ফ্লোৰ": "floor",
    "চিল": "ceil",
    "গুণ": "goon",
    "বাকী": "baki",
    "মূল": "mul",
    "পাই": "pi",
    
    "ৰেণ্ডম": "random",
    "সময়": "xomoy",
    "ফাইল_পঢ়া": "file_poha",
    "ফাইল_লিখা": "file_likha",
    "http_লোৱা": "http_lua",
    
    "ট্ৰাই": "try",
    "ভুল": "bhul",
    "হলে": "hole",
    "শেষ": "xekh",
    
    "অনা": "ona",

    # ── Assamese-first boolean / logic / reassignment keywords (Phase 3) ─────────
    "সঁচা": "xosa",    # True  (xahi)
    "মিথা": "misa",   # False (mitha)
    "নাই":  "nai",     # None  (nai)
    "আৰু":  "aru",     # and   (aru)
    "নহয়": "nohoi",   # not   (nohoi)
    "সলা":  "xola",    # reassign keyword (sali)
}

KEYWORDS = {
    # core
    "dhora", "kua", "lua", "kaam", "return",
    # reassignment (Phase 3: pedagogical keyword, distinguishes first-use from update)
    "sali",
    # conditions
    "jodi", "nohole", "ba", "tetia",
    "xoman", "hoi", "koi", "besi", "kom",
    # loops
    "bare", "kora", "jetialoike",
    "bar", "break", "continue",
    # block delimiters
    "homapto",
    # list & dict
    "list", "dict",
    "log_kora", "del_kora", "loa",
    "len_jukha", "sort",
    "ase", "t",
    # string ops
    "upor", "tol", "kata",
    "gusua", "Lgusua", "Rgusua",
    "bisara", "nidiya", "dighol",
    # math
    "mojiya", "floor", "ceil",
    "goon", "baki", "mul", "pi",
    # stdlib
    "random", "xomoy",
    "file_poha", "file_likha", "http_lua",
    # error handling
    "try", "bhul", "hole", "xekh",
    # import
    "ona",
    # Assamese-first boolean / logic keywords (Phase 3)
    "xosa",    # True  (সঁচা)
    "misa",   # False (মিথা)
    "nai",     # None  (নাই)
    "aru",     # and   (আৰু)
    "naiba",  # or    (নহলে)
    "nohoi",   # not   (নহয়)
    # Python passthrough aliases (legacy — still work for backward compatibility)
    "True", "False", "None",
    "and", "or", "not", "in", "is",
} | set(ASSAMESE_TO_ROMANIZED_KEYWORDS.keys())


@dataclass
class Token:
    type: TT
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"


class TokenizeError(Exception):
    def __init__(self, line: int, col: int, message: str, line_text: str = "", filename: str = ""):
        super().__init__(f"Line {line}: {message}")
        self.line = line
        self.col = col
        self.message = message
        self.line_text = line_text
        self.filename = filename

    def format_error(self) -> str:
        parts = ["", "oi! bhul ase:"]
        if self.filename:
            parts.append(f"  file    : {self.filename}")
        parts.append(f"  line    : {self.line}")
        if self.line_text:
            parts.append(f"  code    : {self.line_text.strip()}")
        parts.append(f"  kiba nai: {self.message}")
        parts.append("")
        parts.append(f"Arey bhai!, Line {self.line}-t eitu ki likhisa? Bhal ke sua! ({self.message})")

        parts.append("")
        return "\n".join(parts)


TOKEN_SPEC = [
    ("SKIP",        r"[ \t]+"),
    ("COMMENT",     r"///.*?///|//[^\n]*"),
    ("NUMBER",      r"\d+(\.\d+)?"),
    ("STRING",      r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''),
    ("PLUS_ASSIGN", r"\+="),
    ("MINUS_ASSIGN",r"-="),
    ("STAR_ASSIGN", r"\*="),
    ("SLASH_ASSIGN",r"/="),
    ("NEQ",         r"!="),
    ("EQ",          r"=="),
    ("LTE",         r"<="),
    ("GTE",         r">="),
    ("LT",          r"<"),
    ("GT",          r">"),
    ("ASSIGN",      r"="),
    ("PLUS",        r"\+"),
    ("MINUS",       r"-"),
    ("STAR",        r"\*"),
    ("SLASH",       r"/"),
    ("PERCENT",     r"%"),
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("LBRACKET",    r"\["),
    ("RBRACKET",    r"\]"),
    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("COMMA",       r","),
    ("COLON",       r":"),
    ("DOT",         r"\."),
    ("NEWLINE",     r"\n"),
    ("IDENT",       r"[A-Za-z_\u0900-\u09FF][A-Za-z0-9_\u0900-\u09FF]*"),
    ("MISMATCH",    r"."),
]

MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC),
    re.DOTALL,
)


def tokenize(code: str, filename: str = "") -> list[Token]:
    tokens: list[Token] = []
    lines = code.splitlines()
    line_num = 1
    line_start = 0
    indent_stack = [0]

    i = 0
    while i < len(code):
        # handle indentation at start of each line
        if i == line_start or (i > 0 and code[i - 1] == "\n"):
            line_start = i
            # count leading spaces
            spaces = 0
            while i + spaces < len(code) and code[i + spaces] == " ":
                spaces += 1

            # skip blank lines and comment-only lines
            rest = code[i + spaces:].lstrip(" \t")
            if rest.startswith("\n") or rest.startswith("\r\n") or rest == "" or rest.startswith("//"):
                pass
            elif code[i + spaces] == "\t":
                raise TokenizeError(
                    line_num, spaces,
                    "tab dile kaam nohoi bhai, space use kora",
                    lines[line_num - 1] if line_num <= len(lines) else "",
                    filename,
                )
            else:
                current_indent = indent_stack[-1]
                if spaces > current_indent:
                    indent_stack.append(spaces)
                    tokens.append(Token(TT.INDENT, "", line_num, spaces))
                while spaces < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(Token(TT.DEDENT, "", line_num, spaces))

        m = MASTER_RE.match(code, i)
        if not m:
            i += 1
            continue

        kind = m.lastgroup
        value = m.group()
        col = i - line_start + 1

        if kind == "SKIP":
            pass
        elif kind == "COMMENT":
            pass
        elif kind == "NEWLINE":
            tokens.append(Token(TT.NEWLINE, value, line_num, col))
            line_num += 1
            line_start = i + 1
        elif kind == "MISMATCH":
            raise TokenizeError(
                line_num, col,
                f"ei character ta Ooju-t nai: {value!r}",
                lines[line_num - 1] if line_num <= len(lines) else "",
                filename,
            )
        elif kind == "NUMBER":
            tokens.append(Token(TT.NUMBER, value, line_num, col))
        elif kind == "STRING":
            tokens.append(Token(TT.STRING, value, line_num, col))
        elif kind == "IDENT":
            if value in ASSAMESE_TO_ROMANIZED_KEYWORDS:
                value = ASSAMESE_TO_ROMANIZED_KEYWORDS[value]
            tt = TT.KEYWORD if value in KEYWORDS else TT.IDENT
            tokens.append(Token(tt, value, line_num, col))
        else:
            tt = TT[kind]
            tokens.append(Token(tt, value, line_num, col))

        i = m.end()

    # close remaining indents
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token(TT.DEDENT, "", line_num, 0))

    tokens.append(Token(TT.EOF, "", line_num, 0))
    return tokens
