from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Diagnostic:
    code: str
    title: str
    line: int
    column: int | None
    snippet: str
    problem: str
    bujha: str
    thik_kora: list[str]
    udaharan: str | None = None
    filename: str = ""


def build_diagnostic(error) -> Diagnostic:
    message = getattr(error, "message", str(error))
    line = getattr(error, "line_number", getattr(error, "line", 0))
    column = getattr(error, "col", None)
    snippet = getattr(error, "line_text", "") or ""
    filename = getattr(error, "filename", "") or ""

    if message.startswith("'dhora ") and "' ৰ পিছত '=' lage" in message:
        return Diagnostic(
            code="missing_assign_after_dhora",
            title="`dhora` line-tu adha thaki gol",
            line=line,
            column=column,
            snippet=snippet,
            problem="Variable bonabo bisarisa, kintu value dibole `=` nai.",
            bujha="Ooju-t `dhora` use korile variable name-r pisot `=` aru ekta value thakibo lage.",
            thik_kora=[
                "`dhora naam = \"Prabal\"` nisina likha.",
                "Jodi value etiya najana, tobu `=`-r pisot kisu value diya.",
            ],
            udaharan='dhora naam = "Prabal"',
            filename=filename,
        )

    if message == "condition ৰ শেষত ':' লাগে":
        return Diagnostic(
            code="missing_colon_after_condition",
            title="condition-r sesot colon nai",
            line=line,
            column=column,
            snippet=snippet,
            problem="Condition line sesh koribole `:` dibo lagisil.",
            bujha="`jodi ... tetia:` ba `nohole jodi ... tetia:` line-r sesot colon thakile next block bujhibole Ooju-r xubidha hoi.",
            thik_kora=[
                "Line-r sesot `:` diya.",
                "Tar pisot next line-t block start kora.",
            ],
            udaharan="jodi (x > 5) hoi, tetia:",
            filename=filename,
        )

    if "বন্ধ কৰা নাই ')'" in message:
        return Diagnostic(
            code="unclosed_parenthesis",
            title="bracket bondho nohoi",
            line=line,
            column=column,
            snippet=snippet,
            problem="Open `(` use kora hoise, kintu tar matching `)` nai.",
            bujha="Function call ba expression-r majot opening bracket thakile closing bracket-o thakibo lage.",
            thik_kora=[
                "Sesot ekta `)` diya.",
                "Bracket count ebar milai saa.",
            ],
            udaharan='dhora naam = lua("tomar naam ki?")',
            filename=filename,
        )

    return Diagnostic(
        code="generic_syntax_error",
        title="syntax line-t kisu golmal ase",
        line=line,
        column=column,
        snippet=snippet,
        problem="Ki bhul hoise, Ooju-e etiya ei line-tu bujhi pua nai.",
        bujha="Ei line-t syntax rule-r logot mil nai, karone parse nohoi.",
        thik_kora=[
            "Line-tu aru ebar bhalke saa.",
            "Bracket, colon, aru keyword order thik ase niki check kora.",
        ],
        filename=filename,
    )


def render_diagnostic(diagnostic: Diagnostic) -> str:
    parts = [""]
    parts.append(f"oi! {diagnostic.title}")

    if diagnostic.filename:
        parts.append(f"file: {diagnostic.filename}")
    parts.append(f"line: {diagnostic.line}")

    if diagnostic.snippet:
        parts.append(f"code: {diagnostic.snippet}")

    parts.append(f"ki bhul hoise: {diagnostic.problem}")
    parts.append(f"bujha: {diagnostic.bujha}")

    for index, fix in enumerate(diagnostic.thik_kora, 1):
        parts.append(f"thik kora {index}: {fix}")

    if diagnostic.udaharan:
        parts.append(f"udaharan: {diagnostic.udaharan}")

    parts.append("")
    return "\n".join(parts)
