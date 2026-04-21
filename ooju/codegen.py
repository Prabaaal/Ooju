from ooju.parser import (
    AssignNode, PrintNode, InputNode, FunctionDefNode, ReturnNode,
    IfNode, ElifClause, ForNode, ForEachNode, WhileNode, DoWhileNode,
    ListDeclNode, ListOpNode, LenNode, RawNode, StringOpNode,
    MathOpNode, DictDeclNode, DictOpNode, StdlibNode, ImportNode,
    TryCatchNode, BreakNode, ContinueNode, AugAssignNode
)


def generate(nodes: list, indent: int = 0) -> tuple[str, dict]:
    """Returns (python_code, sourcemap) where sourcemap[py_line] = oj_line"""
    lines = []
    sourcemap = {}   # python line number → ooju line number
    preamble: list[str] = []  # top-level imports that must stay at top
    pad = "    " * indent

    def add(line_str: str, oj_line: int = 0):
        lines.append(line_str)
        if oj_line:
            sourcemap[len(lines)] = oj_line

    def require_preamble(line_str: str) -> None:
        if indent != 0:
            return
        if line_str not in preamble:
            preamble.append(line_str)

    def extend_block(block_code: str, block_map: dict, fallback_line: str, fallback_oj_line: int) -> None:
        """Extend `lines` with a multi-line block while keeping sourcemap aligned."""
        if block_code and block_code.strip():
            base = len(lines)
            for py_ln, oj_ln in block_map.items():
                # child maps are 1-based line numbers within their own output
                sourcemap[base + py_ln] = oj_ln
            lines.extend(block_code.splitlines())
        else:
            add(fallback_line, fallback_oj_line)

    for node in nodes:
        if isinstance(node, AssignNode):
            add(f"{pad}{node.name} = {node.value}", node.line)

        elif isinstance(node, AugAssignNode):
            add(f"{pad}{node.name} {node.op} {node.value}", node.line)

        elif isinstance(node, PrintNode):
            add(f"{pad}print({node.args})", node.line)

        elif isinstance(node, InputNode):
            add(f"{pad}{node.name} = input({node.prompt})", node.line)

        elif isinstance(node, LenNode):
            add(f"{pad}{node.result} = len({node.target})", node.line)

        elif isinstance(node, ListDeclNode):
            add(f"{pad}{node.name} = {node.items}", node.line)

        elif isinstance(node, ListOpNode):
            if node.op == "log_kora":
                add(f"{pad}{node.var}.append({node.arg})", node.line)
            elif node.op == "del_kora":
                add(f"{pad}{node.var}.remove({node.arg})", node.line)

        elif isinstance(node, StringOpNode):
            if node.op == "upor":
                add(f"{pad}{node.var} = {node.var}.upper()", node.line)
            elif node.op == "tol":
                add(f"{pad}{node.var} = {node.var}.lower()", node.line)
            elif node.op == "kata":
                if len(node.args) == 2:
                    add(f"{pad}{node.var} = {node.var}[{node.args[0]}:{node.args[1]}]", node.line)
                else:
                    add(f"{pad}{node.var} = {node.var}[{node.args[0]}:]", node.line)
            elif node.op == "gusua":
                add(f"{pad}{node.var} = {node.var}.strip()", node.line)
            elif node.op == "Lgusua":
                add(f"{pad}{node.var} = {node.var}.lstrip()", node.line)
            elif node.op == "Rgusua":
                add(f"{pad}{node.var} = {node.var}.rstrip()", node.line)
            elif node.op == "bisara":
                add(f"{pad}{node.var} = {node.var}.find({node.args[0]})", node.line)
            elif node.op == "nidiya":
                add(f"{pad}{node.var} = {node.var}.replace({node.args[0]}, {node.args[1]})", node.line)
            elif node.op == "dighol":
                add(f"{pad}{node.var} = len({node.var})", node.line)

        elif isinstance(node, MathOpNode):
            require_preamble("import math")

            if node.op in ("mojiya", "floor"):
                expr = f"math.floor({node.args[0]})"
            elif node.op == "ceil":
                expr = f"math.ceil({node.args[0]})"
            elif node.op == "mul":
                expr = f"math.sqrt({node.args[0]})"
            elif node.op == "goon":
                expr = f"math.pow({node.args[0]}, {node.args[1]})"
            elif node.op == "baki":
                expr = f"({node.args[0]} % {node.args[1]})"
            elif node.op == "pi":
                expr = "math.pi"
            else:
                expr = f"{node.op}({', '.join(node.args)})"

            if node.result:
                add(f"{pad}{node.result} = {expr}", node.line)
            else:
                add(f"{pad}{expr}", node.line)

        elif isinstance(node, DictDeclNode):
            add(f"{pad}{node.name} = {node.items}", node.line)

        elif isinstance(node, DictOpNode):
            if node.op == "log_kora":
                add(f"{pad}{node.var}[{node.args[0]}] = {node.args[1]}", node.line)
            elif node.op == "del_kora":
                add(f"{pad}del {node.var}[{node.args[0]}]", node.line)
            elif node.op == "loa":
                if node.result:
                    add(f"{pad}{node.result} = {node.var}[{node.args[0]}]", node.line)
                else:
                    add(f"{pad}{node.var}[{node.args[0]}]", node.line)

        elif isinstance(node, StdlibNode):
            import_map = {
                "random": "import random",
                "xomoy":     "from datetime import datetime",
                "http_lua":  "import urllib.request",
            }
            if node.func in import_map:
                require_preamble(import_map[node.func])

            if node.func == "random":
                expr = f"random.randint({node.args[0]}, {node.args[1]})"
            elif node.func == "xomoy":
                expr = "datetime.now()"
            elif node.func == "file_poha":
                expr = f"open({node.args[0]}).read()"
            elif node.func == "file_likha":
                expr = f"open({node.args[0]}, 'w').write({node.args[1]})"
            elif node.func == "http_lua":
                expr = f"urllib.request.urlopen({node.args[0]}).read()"
            else:
                expr = f"{node.func}({', '.join(node.args)})"

            if node.result:
                add(f"{pad}{node.result} = {expr}", node.line)
            else:
                add(f"{pad}{expr}", node.line)

        elif isinstance(node, FunctionDefNode):
            add(f"{pad}def {node.name}({node.args}):", node.line)
            if node.body:
                last = node.body[-1]
                body_nodes = node.body[:]
                # Shortcut 4: implicit return if last node is raw expression
                if isinstance(last, RawNode) and not isinstance(last, (
                    AssignNode, PrintNode, InputNode, ReturnNode,
                    IfNode, ForNode, ForEachNode, WhileNode, DoWhileNode,
                    FunctionDefNode, ListOpNode, StringOpNode, MathOpNode,
                    TryCatchNode, AugAssignNode
                )):
                    body_nodes[-1] = ReturnNode(last.code, last.line)
                
                body_code, body_map = generate(body_nodes, indent + 1)
                extend_block(body_code, body_map, f"{pad}    pass", node.line)
            else:
                add(f"{pad}    pass", node.line)

        elif isinstance(node, ReturnNode):
            add(f"{pad}return {node.value}", node.line)

        elif isinstance(node, IfNode):
            add(f"{pad}if {node.condition}:", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, f"{pad}    pass", node.line)
            
            for elif_clause in node.elifs:
                add(f"{pad}elif {elif_clause.condition}:", elif_clause.line)
                elif_body_code, elif_body_map = generate(elif_clause.body, indent + 1)
                extend_block(elif_body_code, elif_body_map, f"{pad}    pass", elif_clause.line)
                
            if node.else_body:
                add(f"{pad}else:", node.line)
                else_body_code, else_body_map = generate(node.else_body, indent + 1)
                extend_block(else_body_code, else_body_map, f"{pad}    pass", node.line)

        elif isinstance(node, ForNode):
            add(f"{pad}for _ in range({node.count}):", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, f"{pad}    pass", node.line)

        elif isinstance(node, ForEachNode):
            add(f"{pad}for {node.item} in {node.iterable}:", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, f"{pad}    pass", node.line)

        elif isinstance(node, WhileNode):
            add(f"{pad}while {node.condition}:", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, f"{pad}    pass", node.line)

        elif isinstance(node, DoWhileNode):
            add(f"{pad}while True:", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, "", 0)
            add(f"{pad}    if not ({node.condition}): break", node.line)

        elif isinstance(node, TryCatchNode):
            add(f"{pad}try:", node.line)
            body_code, body_map = generate(node.body, indent + 1)
            extend_block(body_code, body_map, f"{pad}    pass", node.line)
            
            if node.catch_body:
                add(f"{pad}except Exception as {node.error_var}:", node.line)
                catch_code, catch_map = generate(node.catch_body, indent + 1)
                extend_block(catch_code, catch_map, f"{pad}    pass", node.line)
                
            if node.finally_body:
                add(f"{pad}finally:", node.line)
                finally_code, finally_map = generate(node.finally_body, indent + 1)
                extend_block(finally_code, finally_map, f"{pad}    pass", node.line)

        elif isinstance(node, ImportNode):
            add(f"{pad}# imported from: {node.path}", node.line)
            try:
                from pathlib import Path
                imported_code = Path(node.path).read_text(encoding="utf-8")
                from ooju.tokenizer import tokenize
                from ooju.parser import parse
                imported_tokens = tokenize(imported_code, node.path)
                imported_ast = parse(imported_tokens, node.path)
                imported_py, imported_map = generate(imported_ast, indent)
                extend_block(imported_py, imported_map, f"{pad}    pass", node.line)
            except FileNotFoundError:
                add(f"{pad}# oi! '{node.path}' file tu bisari pua nai", node.line)

        elif isinstance(node, BreakNode):
            add(f"{pad}break", node.line)
            
        elif isinstance(node, ContinueNode):
            add(f"{pad}continue", node.line)

        elif isinstance(node, RawNode):
            add(f"{pad}{node.code}", node.line)

    if indent == 0 and preamble:
        shifted = {py_ln + len(preamble): oj_ln for py_ln, oj_ln in sourcemap.items()}
        return "\n".join([*preamble, *lines]), shifted
    return "\n".join(lines), sourcemap
