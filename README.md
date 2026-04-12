<div align="center">

<img src="assets/ooju-logo.png" alt="Ooju logo — Bengali উজু in a glass sphere" width="220" />

# Ooju · উজু

**A beginner-friendly programming language written in Assamese**

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen?style=flat-square)](https://github.com/Prabaaal/Ooju/releases)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-success?style=flat-square)](#)

> *"Programming, made natural in Assamese"*

Ooju (উজু — meaning *easy*) is a transpiled language that lets beginners write programs using Assamese keywords, lowering the barrier to coding for Assamese-speaking communities. It transpiles cleanly to Python through a full **Tokenizer → Parser → Code Generator** pipeline.

</div>

---

## ✨ Features

- 🗣️ **Assamese keywords** — write code in your own language
- ⚡ **Runs on Python** — zero extra runtime needed
- 🛠️ **CLI tools** — `run`, `compile`, `repl`, and `version`
- 🔒 **Safe execution** — sandboxed builtins, no `exec` surprises
- 🎨 **VS Code support** — syntax highlighting for `.oj` files
- 📚 **Teaching-friendly** — clear, helpful error messages

---

## 📦 Installation

```bash
pip install ooju
```

### Development Setup

```bash
git clone https://github.com/Prabaaal/Ooju.git
cd Ooju
pip install -e .
```

---

## 🚀 Quick Start

Create a file called `hello.oj`:

```
kaam greet(name):
    kua("Namaskar, " + name)

dhora naam = lobo("Tomar naam ki? ")
greet(naam)
```

Run it:

```bash
ooju run hello.oj
```

See the generated Python:

```bash
ooju run hello.oj --debug
```

Compile to a `.py` file:

```bash
ooju compile hello.oj
```

---

## 📖 Language Reference

### Variables
```
dhora x = 5
dhora greet = "Namaskar!"
```

### Output & Input
```
kua("Namaskar!")          # print
dhora name = lobo("Ki?)   # input
```

### Functions
```
kaam add(a, b):
    return a + b
```

### Conditionals
```
jodi (x > 5) hoi, tetia:
    kua("besi")
nohole jodi (x > 3) hoi, tetia:
    kua("moddhyom")
nohole ba:
    kua("kom")
```

### Loops
```
# Repeat N times
3 bar kora:
    kua("hello")

# While loop
jetialoike (x < 10) bare bare kora:
    dhora x = x + 1
```

### Comments
```
// This is a single-line comment

///
This is a
block comment
///
```

---

## ⚠️ Error Messages

Ooju gives beginner-friendly errors with context and suggestions:

```
OojuError:
  File : hello.oj
  Line : 3
  Code : dhora naam
  Issue: missing assignment after 'dhora'
  Help : Did you mean: dhora x = 10 ?
```

---

## 📂 Project Structure

```
Ooju/
├── assets/             # Branding (logo)
├── ooju/               # Core language package
│   ├── tokenizer.py    # Lexer — text → tokens
│   ├── parser.py       # Parser — tokens → AST
│   ├── codegen.py      # Code generator — AST → Python
│   ├── transpiler.py   # Pipeline orchestrator
│   ├── cli.py          # Command-line interface
│   ├── repl.py         # Interactive REPL
│   └── stdlib.py       # Safe builtins sandbox
├── examples/           # Sample .oj programs
├── tests/              # Pytest test suite
├── editors/vscode/     # VS Code syntax extension
├── pyproject.toml
└── README.md
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/
```

---

## 🎨 Editor Support

Syntax highlighting for `.oj` files is available for **VS Code**.

```bash
cd editors/vscode
npm install
npm run package          # builds the .vsix
code --install-extension ooju-vscode-*.vsix
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

Please ensure all tests pass before submitting.

---

## 📄 License

MIT © [Prabal Gogoi](https://github.com/Prabaaal)

---

<div align="center">
Made with ❤️ for Assamese learners
</div>
