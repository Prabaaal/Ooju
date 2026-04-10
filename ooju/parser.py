from dataclasses import dataclass
from typing import Any, List
from ooju.tokenizer import Token, TT, TokenizeError

# ─── AST Nodes ────────────────────────────────────────────────────────────────

@dataclass
class AssignNode:
    name: str
    value: str
    line: int

@dataclass
class AugAssignNode:
    name: str
    op: str       # += -= *= /=
    value: str
    line: int

@dataclass
class PrintNode:
    args: str
    line: int

@dataclass
class InputNode:
    name: str
    prompt: str
    line: int

@dataclass
class FunctionDefNode:
    name: str
    args: str
    body: list
    line: int

@dataclass
class ReturnNode:
    value: str
    line: int

@dataclass
class IfNode:
    condition: str
    body: list
    elifs: list
    else_body: list
    line: int

@dataclass
class ElifClause:
    condition: str
    body: list
    line: int

@dataclass
class ForNode:
    count: str
    body: list
    line: int

@dataclass
class ForEachNode:
    item: str
    iterable: str
    body: list
    line: int

@dataclass
class WhileNode:
    condition: str
    body: list
    line: int

@dataclass
class DoWhileNode:
    body: list
    condition: str
    line: int

@dataclass
class ListDeclNode:
    name: str
    items: str
    line: int

@dataclass
class ListOpNode:
    var: str
    op: str       # log_kora | del_kora
    arg: str
    line: int

@dataclass
class StringOpNode:
    var: str
    op: str        # upor | tol | kata | gusua | khoja | nidiya | dighol
    args: list
    result: str
    line: int

@dataclass
class MathOpNode:
    op: str
    args: list
    result: str
    line: int

@dataclass
class DictDeclNode:
    name: str
    items: str
    line: int

@dataclass
class DictOpNode:
    var: str
    op: str       # log_kora | del_kora | loa
    args: list
    result: str
    line: int

@dataclass
class StdlibNode:
    func: str
    args: list
    result: str
    line: int

@dataclass
class ImportNode:
    path: str
    line: int

@dataclass
class TryCatchNode:
    body: list
    error_var: str
    catch_body: list
    finally_body: list
    line: int

@dataclass
class BreakNode:
    line: int

@dataclass
class ContinueNode:
    line: int

@dataclass
class LenNode:
    result: str
    target: str
    line: int

@dataclass
class RawNode:
    code: str
    line: int


# ─── Parser ───────────────────────────────────────────────────────────────────

class ParseError(Exception):
    def __init__(self, line: int, message: str, line_text: str = "", filename: str = ""):
        super().__init__(f"Line {line}: {message}")
        self.line = line
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
        parts.append(f"Aarey dada!, Line {self.line}-t eitu ki likhisa? Bhal ke sua! ({self.message})")
        parts.append("")
        return "\n".join(parts)

class MultiParseError(Exception):
    def __init__(self, errors: list[ParseError]):
        self.errors = errors

    def format_error(self) -> str:
        parts = [""]
        parts.append(f"oi! {len(self.errors)}ta bhul ase:\n")
        for i, err in enumerate(self.errors, 1):
            parts.append(f"  [{i}] line {err.line}: {err.message}")
            if err.line_text:
                parts.append(f"      code: {err.line_text.strip()}")
            parts.append("")
        parts.append(f"Aarey dada!, {len(self.errors)}ta bhul ase thik kora! 💪")
        parts.append("")
        return "\n".join(parts)

class Parser:
    def __init__(self, tokens: list[Token], filename: str = ""):
        self.tokens = tokens
        self.pos = 0
        self.filename = filename

    def peek(self, offset=0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[idx]

    def consume(self) -> Token:
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def expect(self, tt: TT, err: str) -> Token:
        t = self.peek()
        if t.type != tt:
            raise ParseError(t.line, err, filename=self.filename)
        return self.consume()

    def skip_newlines(self):
        while self.peek().type == TT.NEWLINE:
            self.consume()

    def collect_expr(self, stop_at_rparen=False) -> str:
        parts = []
        depth = 0
        while self.peek().type not in (TT.NEWLINE, TT.EOF):
            t = self.peek()
            if t.type == TT.COLON and depth == 0:
                break
            if t.type == TT.LPAREN:
                depth += 1
            elif t.type == TT.RPAREN:
                if depth == 0 and stop_at_rparen:
                    break
                depth -= 1
            parts.append(self.consume().value)
        return " ".join(parts).strip()

    def collect_until_newline(self) -> str:
        parts = []
        while self.peek().type not in (TT.NEWLINE, TT.EOF):
            parts.append(self.consume().value)
        return " ".join(parts).strip()

    def parse_block(self) -> list:
        self.skip_newlines()
        self.expect(TT.INDENT, "block start hobo lagisil (indent nai)")
        body = []
        while self.peek().type not in (TT.DEDENT, TT.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        if self.peek().type == TT.DEDENT:
            self.consume()
        return body

    def parse_condition(self) -> str:
        t = self.peek()
        is_elif = t.value == "nohole"

        if is_elif:
            self.consume()  # nohole/nahole
            if self.peek().value == "jodi":
                self.consume()  # jodi
        else:
            self.consume()  # jodi

        if self.peek().type == TT.LPAREN:
            self.consume()
            parts = []
            depth = 1
            while depth > 0 and self.peek().type != TT.EOF:
                tok = self.consume()
                if tok.type == TT.LPAREN:
                    depth += 1
                elif tok.type == TT.RPAREN:
                    depth -= 1
                    if depth == 0:
                        break
                parts.append(tok.value)
            while self.peek().value in ("hoi", "tetia") or self.peek().type == TT.COMMA:
                self.consume()
            self.expect(TT.COLON, "condition ৰ শেষত ':' লাগে")
            return " ".join(parts).strip()

        parts = []
        while self.peek().type not in (TT.EOF, TT.COLON) and self.peek().value not in ("tetia", "hoi"):
            if self.peek().value == "xoman":
                self.consume()
                parts.insert(-1, "==")
                continue
            if self.peek().value == "besi":
                self.consume()
                parts.insert(-1, ">")
                continue
            if self.peek().value == "kom":
                self.consume()
                parts.insert(-1, "<")
                continue
            if self.peek().value in ("t", "koi"):
                self.consume()
                continue
            parts.append(self.consume().value)

        while self.peek().value in ("hoi", "tetia") or self.peek().type == TT.COMMA:
            self.consume()
        self.expect(TT.COLON, "condition ৰ শেষত ':' লাগে")
        return " ".join(parts).strip()

    def parse_statement(self):
        self.skip_newlines()
        t = self.peek()

        if t.type == TT.EOF:
            return None

        if t.type in (TT.DEDENT, TT.INDENT):
            self.consume()
            return None
            
        if t.type == TT.KEYWORD and t.value == "lua":
            self.consume()
            if self.peek().type == TT.IDENT:
                name = self.consume().value
                self.skip_newlines()
                return InputNode(name, '""', t.line)
            raise ParseError(t.line, "'lua' ৰ পিছত variable name লাগে — example: lua naam", filename=self.filename)

        if t.type == TT.KEYWORD and t.value == "dhora":
            self.consume()
            name = self.expect(TT.IDENT, "'dhora' ৰ পিছত variable name lage").value

            if self.peek().type == TT.ASSIGN:
                self.consume()
                if self.peek().value == "lua":
                    self.consume()
                    self.expect(TT.LPAREN, "'lua' ৰ পিছত '(' lage")
                    prompt = self.collect_expr(stop_at_rparen=True)
                    self.expect(TT.RPAREN, "'lua(...)' বন্ধ কৰা নাই ')'")
                    self.skip_newlines()
                    return InputNode(name, prompt, t.line)
                
                if self.peek().value == "len_jukha":
                    self.consume()
                    self.expect(TT.LPAREN, "'len_jukha' ৰ পিছত '(' lage")
                    target = self.expect(TT.IDENT, "list name lage").value
                    self.expect(TT.RPAREN, "'len_jukha(...)' বন্ধ কৰা নাই ')'")
                    self.skip_newlines()
                    return LenNode(name, target, t.line)
                    
                if self.peek().value in ("mojiya", "floor", "ceil", "mul"):
                    op = self.consume().value
                    self.expect(TT.LPAREN, f"'{op}' ৰ পিছত '(' লাগে")
                    arg = self.collect_expr(stop_at_rparen=True)
                    self.expect(TT.RPAREN, f"'{op}(...)' বন্ধ কৰা নাই ')'")
                    self.skip_newlines()
                    return MathOpNode(op, [arg], name, t.line)

                if self.peek().value in ("goon", "baki"):
                    op = self.consume().value
                    self.expect(TT.LPAREN, f"'{op}' ৰ পিছত '(' লাগে")
                    args_raw = self.collect_expr(stop_at_rparen=True)
                    self.expect(TT.RPAREN, f"'{op}(...)' বন্ধ কৰা নাই ')'")
                    parts = [a.strip() for a in args_raw.split(",", 1)]
                    self.skip_newlines()
                    return MathOpNode(op, parts, name, t.line)
                    
                if self.peek().value in ("random", "xomoy", "file_poha", "http_lua"):
                    func = self.consume().value
                    self.expect(TT.LPAREN, f"'{func}' ৰ পিছত '(' লাগে")
                    args_raw = self.collect_expr(stop_at_rparen=True)
                    self.expect(TT.RPAREN, f"'{func}(...)' বন্ধ কৰা নাই ')'")
                    parts = [a.strip() for a in args_raw.split(",")] if args_raw else []
                    self.skip_newlines()
                    return StdlibNode(func, parts, name, t.line)

                value = self.collect_until_newline()
                self.skip_newlines()
                return AssignNode(name, value, t.line)

            raise ParseError(t.line, f"'dhora {name}' ৰ পিছত '=' lage", filename=self.filename)

        if t.type == TT.IDENT and self.peek(1).type in (
            TT.PLUS_ASSIGN, TT.MINUS_ASSIGN, TT.STAR_ASSIGN, TT.SLASH_ASSIGN
        ):
            name = self.consume().value
            op_tok = self.consume()
            op_map = {
                TT.PLUS_ASSIGN:  "+=",
                TT.MINUS_ASSIGN: "-=",
                TT.STAR_ASSIGN:  "*=",
                TT.SLASH_ASSIGN: "/=",
            }
            op = op_map[op_tok.type]
            value = self.collect_until_newline()
            self.skip_newlines()
            return AugAssignNode(name, op, value, t.line)

        if t.type == TT.KEYWORD and t.value == "list":
            self.consume()
            if self.peek().value != "kora":
                raise ParseError(t.line, "'list' ৰ পিছত 'kora' lage", filename=self.filename)
            self.consume()
            name = self.expect(TT.IDENT, "'list kora' ৰ পিছত list name lage").value
            self.expect(TT.ASSIGN, f"'list kora {name}' ৰ পিছত '=' lage")
            items = self.collect_until_newline()
            self.skip_newlines()
            return ListDeclNode(name, items, t.line)

        if t.type == TT.KEYWORD and t.value == "dict":
            self.consume()
            if self.peek().value != "kora":
                raise ParseError(t.line, "'dict' ৰ পিছত 'kora' লাগে", filename=self.filename)
            self.consume()
            name = self.expect(TT.IDENT, "'dict kora' ৰ পিছত dict name লাগে").value
            self.expect(TT.ASSIGN, f"'dict kora {name}' ৰ পিছত '=' লাগে")
            items = self.collect_until_newline()
            self.skip_newlines()
            return DictDeclNode(name, items, t.line)

        if t.type == TT.KEYWORD and t.value == "kua":
            self.consume()
            if self.peek().type != TT.LPAREN:
                args = self.collect_until_newline()
                self.skip_newlines()
                return PrintNode(args, t.line)
            self.expect(TT.LPAREN, "'kua' ৰ পিছত '(' লাগে")
            args = self.collect_expr(stop_at_rparen=True)
            self.expect(TT.RPAREN, "'kua(...)' বন্ধ কৰা নাই ')'")
            self.skip_newlines()
            return PrintNode(args, t.line)

        if t.type == TT.KEYWORD and t.value == "kaam":
            self.consume()
            name = self.expect(TT.IDENT, "'kaam' ৰ পিছত function name lage").value
            self.expect(TT.LPAREN, f"'kaam {name}' ৰ পিছত '(' lage")
            args = self.collect_expr(stop_at_rparen=True)
            self.expect(TT.RPAREN, "function args বন্ধ কৰা নাই ')'")
            self.expect(TT.COLON, f"'kaam {name}(...)' ৰ শেষত ':' lage")
            self.skip_newlines()
            body = self.parse_block()
            return FunctionDefNode(name, args, body, t.line)

        if t.type == TT.KEYWORD and t.value == "return":
            self.consume()
            value = self.collect_until_newline()
            self.skip_newlines()
            return ReturnNode(value, t.line)
            
        if t.type == TT.KEYWORD and t.value == "ona":
            self.consume()
            path_tok = self.expect(TT.STRING, "'ona' ৰ পিছত file path লাগে — example: ona \"utils.oj\"")
            self.skip_newlines()
            return ImportNode(path_tok.value.strip('"\''), t.line)
            
        if t.type == TT.KEYWORD and t.value == "koxa":
            self.consume()
            self.expect(TT.COLON, "'koxa' ৰ শেষত ':' লাগে")
            self.skip_newlines()
            body = self.parse_block()

            error_var = "bhul"
            catch_body = []
            finally_body = []

            if self.peek().value == "dhora":
                self.consume()
                error_var = self.consume().value
                if self.peek().value != "hole":
                    raise ParseError(t.line, "'dhora <name>' ৰ পিছত 'hole:' লাগে", filename=self.filename)
                self.consume()
                self.expect(TT.COLON, "'dhora bhul hole' ৰ শেষত ':' লাগে")
                self.skip_newlines()
                catch_body = self.parse_block()

            if self.peek().value == "xekh":
                self.consume()
                self.expect(TT.COLON, "'xekh' ৰ শেষত ':' লাগে")
                self.skip_newlines()
                finally_body = self.parse_block()

            return TryCatchNode(body, error_var, catch_body, finally_body, t.line)
            
        if t.type == TT.KEYWORD and t.value == "break":
            self.consume()
            self.skip_newlines()
            return BreakNode(t.line)

        if t.type == TT.KEYWORD and t.value == "continue":
            self.consume()
            self.skip_newlines()
            return ContinueNode(t.line)

        if t.type == TT.KEYWORD and t.value == "jodi":
            line = t.line
            condition = self.parse_condition()
            self.skip_newlines()
            body = self.parse_block()
            elifs = []
            else_body = []

            while self.peek().value == "nohole":
                next2 = self.peek(1)
                if next2.value == "jodi":
                    elif_line = self.peek().line
                    elif_cond = self.parse_condition()
                    self.skip_newlines()
                    elif_body = self.parse_block()
                    elifs.append(ElifClause(elif_cond, elif_body, elif_line))
                elif next2.value == "ba":
                    self.consume()
                    self.consume()
                    self.expect(TT.COLON, "'nohole ba' ৰ শেষত ':' lage")
                    self.skip_newlines()
                    else_body = self.parse_block()
                    break
                else:
                    break

            return IfNode(condition, body, elifs, else_body, line)

        if t.type == TT.KEYWORD and t.value == "bare":
            self.consume()
            if self.peek().value != "bare":
                raise ParseError(t.line, "'bare' ৰ পিছত আৰু এটা 'bare' lage", filename=self.filename)
            self.consume()
            if self.peek().value != "kora":
                raise ParseError(t.line, "'bare bare' ৰ পিছত 'kora' lage", filename=self.filename)
            self.consume()
            self.expect(TT.COLON, "'bare bare kora' ৰ শেষত ':' lage")
            self.skip_newlines()
            body = self.parse_block()
            
            # The condition 'jetialoike (cond)' might be the last statement inside the block
            if body and hasattr(body[-1], "is_do_while_cond"):
                cond_stmt = body.pop()
                return DoWhileNode(body, cond_stmt.condition, t.line)
            
            # Or it might be dedented outside the block
            if self.peek().value == "jetialoike":
                self.consume()
                self.expect(TT.LPAREN, "'jetialoike' ৰ পিছত '(' lage")
                condition = self.collect_expr(stop_at_rparen=True)
                self.expect(TT.RPAREN, "'jetialoike (...)' বন্ধ কৰা নাই ')'")
                self.skip_newlines()
                return DoWhileNode(body, condition, t.line)
                
            raise ParseError(t.line, "'bare bare kora:' block বন্ধ কৰিবলৈ 'jetialoike (...)' লাগে", filename=self.filename)

        if t.type == TT.KEYWORD and t.value == "jetialoike":
            self.consume()
            self.expect(TT.LPAREN, "'jetialoike' ৰ পিছত '(' lage")
            condition = self.collect_expr(stop_at_rparen=True)
            self.expect(TT.RPAREN, "'jetialoike (...)' বন্ধ কৰা নাই ')'")
            if self.peek().value != "bare":
                # Might be a do-while condition at the end of a block
                class DoWhileConditionNode:
                    def __init__(self, c, l):
                        self.condition = c
                        self.line = l
                        self.is_do_while_cond = True
                self.skip_newlines()
                return DoWhileConditionNode(condition, t.line)
            self.consume(); self.consume(); self.consume()
            self.expect(TT.COLON, "'bare bare kora' ৰ শেষত ':' lage")
            self.skip_newlines()
            body = self.parse_block()
            return WhileNode(condition, body, t.line)

        if t.type in (TT.NUMBER, TT.IDENT) and self.peek(1).value == "bar":
            count = self.consume().value
            self.consume()
            
            if self.peek().type == TT.COLON:
                self.consume()
                self.skip_newlines()
                body = self.parse_block()
                return ForNode(count, body, t.line)
            
            if self.peek().value == "bare":
                self.consume()
                self.consume()
            
            if self.peek().value == "kora":
                self.consume()
                
            self.expect(TT.COLON, "for loop ৰ শেষত ':' lage")
            self.skip_newlines()
            body = self.parse_block()
            return ForNode(count, body, t.line)

        if t.type == TT.IDENT and self.peek(1).value == "t" and self.peek(2).value == "ase":
            item = self.consume().value
            self.consume()
            self.consume()
            iterable = self.consume().value
            self.consume()
            while self.peek().value in ("tetia",) or self.peek().type == TT.COMMA:
                self.consume()
            self.expect(TT.COLON, "for-each loop ৰ শেষত ':' lage")
            self.skip_newlines()
            body = self.parse_block()
            return ForEachNode(item, iterable, body, t.line)

        if t.type == TT.IDENT and self.peek(1).type == TT.DOT:
            var = self.consume().value
            self.consume()
            op = self.consume().value
            
            if op in ("log_kora", "del_kora", "loa"):
                self.expect(TT.LPAREN, f"'{op}' ৰ পিছত '(' lage")
                args_raw = self.collect_expr(stop_at_rparen=True)
                self.expect(TT.RPAREN, f"'{op}(...)' বন্ধ কৰা নাই ')'")
                self.skip_newlines()

                parts = [a.strip() for a in args_raw.split(",", 1)]

                if op == "loa":
                    return DictOpNode(var, op, parts, "", t.line)
                elif op == "log_kora" and len(parts) == 2:
                    return DictOpNode(var, op, parts, "", t.line)
                elif op == "del_kora" and len(parts) == 1:
                    # could be list remove or dict del — handled in codegen by context
                    return ListOpNode(var, op, parts[0], t.line)
                else:
                    return ListOpNode(var, op, parts[0], t.line)
            elif op in ("upor", "tol", "gusua", "Lgusua", "Rgusua"):
                self.expect(TT.LPAREN, f"'{op}' ৰ পিছত '(' লাগে")
                self.expect(TT.RPAREN, f"'{op}()' বন্ধ কৰা নাই ')'")
                self.skip_newlines()
                return StringOpNode(var, op, [], "", t.line)
            elif op == "kata":
                self.expect(TT.LPAREN, "'kata' ৰ পিছত '(' লাগে")
                start = self.collect_expr(stop_at_rparen=True).split(",")[0].strip()
                if self.peek().type == TT.COMMA:
                    self.consume()
                end = self.collect_expr(stop_at_rparen=True).strip()
                self.expect(TT.RPAREN, "'kata(...)' বন্ধ কৰা নাই ')'")
                self.skip_newlines()
                return StringOpNode(var, op, [start, end], "", t.line)
            elif op == "khoja":
                self.expect(TT.LPAREN, "'khoja' ৰ পিছত '(' লাগে")
                arg = self.collect_expr(stop_at_rparen=True)
                self.expect(TT.RPAREN, "'khoja(...)' বন্ধ কৰা নাই ')'")
                self.skip_newlines()
                return StringOpNode(var, op, [arg], "", t.line)
            elif op == "nidiya":
                self.expect(TT.LPAREN, "'nidiya' ৰ পিছত '(' লাগে")
                args_raw = self.collect_expr(stop_at_rparen=True)
                self.expect(TT.RPAREN, "'nidiya(...)' বন্ধ কৰা নাই ')'")
                parts = [a.strip() for a in args_raw.split(",", 1)]
                self.skip_newlines()
                return StringOpNode(var, op, parts, "", t.line)
            elif op == "dighol":
                self.expect(TT.LPAREN, "'dighol' ৰ পিছত '(' লাগে")
                self.expect(TT.RPAREN, "'dighol()' বন্ধ কৰা নাই ')'")
                self.skip_newlines()
                return StringOpNode(var, op, [], "", t.line)
            else:
                raw = self.collect_until_newline()
                self.skip_newlines()
                return RawNode(f"{var}.{op}{raw}", t.line)

        raw = self.collect_until_newline()
        self.skip_newlines()
        if raw:
            return RawNode(raw, t.line)
        return None


def parse(tokens: list[Token], filename: str = "", collect_errors: bool = False) -> list:
    parser = Parser(tokens, filename)
    nodes = []
    errors = []
    parser.skip_newlines()
    while parser.peek().type != TT.EOF:
        try:
            stmt = parser.parse_statement()
            if stmt:
                nodes.append(stmt)
        except ParseError as e:
            if collect_errors:
                errors.append(e)
                # primitive sync: skip to next newline
                while parser.peek().type not in (TT.NEWLINE, TT.EOF):
                    parser.consume()
                parser.skip_newlines()
            else:
                raise
    if errors:
        raise MultiParseError(errors)
    return nodes
