<p align="center">
  <img src="assets/logo.png" alt="Ooju Logo" width="180"/>
</p>

<h1 align="center">Ooju — Assamese Programming Language</h1>

<p align="center">
  Write code in Assamese. Run it like Python.
</p>

---

## What is Ooju?

**Ooju** is a beginner-friendly programming language inspired by Assamese syntax.

It supports both Assamese script:

```ooju
ধৰা x = 10
কোৱা(x)
````

and romanized Assamese:

```ooju
dhora x = 10
kua(x)
```

Ooju converts your code into Python and executes it using Python’s runtime.

```txt
Ooju Code → Tokenizer → Parser → AST → Python Code → Execution
```

---

## Why Ooju?

Programming often forces beginners to think in English before they can think in logic.

Ooju tries to make programming feel closer to Assamese thinking.

* Code in Assamese script or romanized Assamese
* Beginner-friendly syntax
* Python-powered execution
* Real tokenizer, parser, AST, and code generator
* CLI runner, compiler, syntax checker, debug mode, and REPL
* Supports variables, functions, conditions, loops, lists, dictionaries, strings, math, file operations, imports, and error handling
* Supports indentation, `সমাপ্ত`, and `{ }` block styles

---

## Quick Example

```ooju
ধৰা নাম = লোৱা("তোমাৰ নাম কি? ")

যদি নাম == "Prabal" তেতিয়া:
    কোৱা "Welcome back!"
নহলে বা:
    কোৱা "Hello " + নাম
```

Equivalent Python:

```python
naam = input("তোমাৰ নাম কি? ")

if naam == "Prabal":
    print("Welcome back!")
else:
    print("Hello " + naam)
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Prabaaal/Ooju.git
cd Ooju
```

Install locally:

```bash
pip install -e .
```

Check the installed version:

```bash
ooju version
```

---

## CLI Usage

Ooju includes a command-line interface for running, compiling, checking, debugging, and using the REPL.

### Run a file

```bash
ooju run examples/hello.oj
```

You can also run a file directly:

```bash
ooju examples/hello.oj
```

---

### Compile Ooju to Python

```bash
ooju compile examples/hello.oj
```

This generates a `.py` file next to the source file.

You can also choose the output path:

```bash
ooju compile examples/hello.oj -o hello.py
```

---

### Check syntax

```bash
ooju check examples/hello.oj
```

If everything is valid:

```txt
sob thik ase! no syntax errors found. ✅
```

---

### Debug mode

Use `--debug` to see the generated Python code.

```bash
ooju run examples/hello.oj --debug
```

Example output:

```txt
Transpiled Python:
------------------
name = input("Enter name: ")
print("Hello " + name)
```

---

### REPL

Start the interactive Ooju shell:

```bash
ooju repl
```

Example:

```txt
ooju> ধৰা x = 10
ooju> কোৱা x
10
```

Exit the REPL with:

```txt
jau
```

or:

```txt
exit
quit
oba
```

---

## Language Features

### Variables

```ooju
ধৰা x = 10
ধৰা নাম = "Prabal"
```

Romanized:

```ooju
dhora x = 10
dhora naam = "Prabal"
```

---

### Reassignment

Ooju supports explicit reassignment using `সলা` / `xola`.

```ooju
ধৰা x = 10
sola x = 20
```

Romanized:

```ooju
dhora x = 10
xola x = 20
```

---

### Output

```ooju
কোৱা("Hello")
```

Beginner-friendly shortcut:

```ooju
কোৱা "Hello"
```

Romanized:

```ooju
kua "Hello"
```

---

### Input

```ooju
ধৰা নাম = লোৱা("Enter name: ")
```

Shortcut:

```ooju
লোৱা নাম
```

Romanized:

```ooju
lua naam
```

---

## Conditions

```ooju
যদি x > 10 তেতিয়া:
    কোৱা "ডাঙৰ"
নহলে যদি x == 10 তেতিয়া:
    কোৱা "সমান"
নহলে বা:
    কোৱা "সৰু"
```

Romanized:

```ooju
jodi x > 10 tetia:
    kua "big"
nohole jodi x == 10 tetia:
    kua "equal"
nohole ba:
    kua "small"
```

Ooju also supports Assamese-style comparison patterns:

```ooju
যদি x 10ত কৈ বেছি হয়, তেতিয়া:
    কোৱা "x is greater"
```

---

## Functions

```ooju
কাম যোগ(a, b):
    ঘুৰা a + b
```

Romanized:

```ooju
kaam jog(a, b):
    return a + b
```

Ooju also supports implicit return for the last raw expression in a function:

```ooju
কাম যোগ(a, b):
    a + b
```

---

## Loops

### Repeat loop

```ooju
5 বাৰ কৰা:
    কোৱা "Hello"
```

Romanized:

```ooju
5 bar kora:
    kua "Hello"
```

---

### While loop

```ooju
যেতিয়ালৈকে (x < 5) বাৰে বাৰে কৰা:
    কোৱা x
    x += 1
```

---

### Do-while loop

```ooju
বাৰে বাৰে কৰা:
    কোৱা x
    x += 1
যেতিয়ালৈকে (x < 5)
```

---

### For-each loop

```ooju
item ত আছে items তেতিয়া:
    কোৱা item
```

---

## Block Syntax

Ooju supports three block styles.

### 1. Indentation style

```ooju
যদি x > 5 তেতিয়া:
    কোৱা "big"
```

### 2. Explicit end style

```ooju
যদি x > 5 তেতিয়া:
কোৱা "big"
সমাপ্ত
```

### 3. Bracket style

```ooju
যদি x > 5 তেতিয়া {
    কোৱা "big"
}
```

This allows Ooju to feel natural for beginners while still being comfortable for programmers coming from C, Java, or JavaScript.

---

## Lists

```ooju
list কৰা nums = [1, 2, 3]

nums.লগ_কৰা(4)
nums.ডেল_কৰা(2)

কোৱা nums
```

Romanized:

```ooju
list kora nums = [1, 2, 3]

nums.log_kora(4)
nums.del_kora(2)

kua nums
```

---

## Dictionaries

```ooju
dict কৰা student = {"name": "Prabal", "age": 21}

student.লগ_কৰা("city", "Assam")
কোৱা student
```

Romanized:

```ooju
dict kora student = {"name": "Prabal", "age": 21}

student.log_kora("city", "Assam")
kua student
```

---

## String Operations

```ooju
ধৰা নাম = "prabal"

নাম.ওপৰ()
কোৱা নাম
```

Available operations:

| Assamese | Romanized | Meaning   |
| -------- | --------- | --------- |
| ওপৰ      | upor      | uppercase |
| তল       | tol       | lowercase |
| কটা      | kata      | slice     |
| গুচোৱা   | gusua     | strip     |
| বিচৰা    | bisara    | find      |
| নিদিয়া   | nidiya    | replace   |
| দীঘল     | dighol    | length    |

---

## Math Operations

```ooju
ধৰা x = মূল(25)
ধৰা y = গুণ(2, 3)
ধৰা z = বাকী(10, 3)

কোৱা x
কোৱা y
কোৱা z
```

Available operations:

| Assamese | Romanized | Meaning     |
| -------- | --------- | ----------- |
| মূল      | mul       | square root |
| গুণ      | goon      | power       |
| বাকী     | baki      | modulo      |
| মজিয়া    | mojiya    | floor       |
| চিল      | ceil      | ceil        |
| পাই      | pi        | pi value    |

---

## Standard Library Helpers

```ooju
ধৰা n = ৰেণ্ডম(1, 10)
কোৱা n

ধৰা এতিয়া = সময়()
কোৱা এতিয়া
```

Supported helpers:

| Assamese  | Romanized  | Meaning             |
| --------- | ---------- | ------------------- |
| ৰেণ্ডম    | random     | random number       |
| সংখ্যা    | xankhya    | random number alias |
| সময়       | xomoy      | current time        |
| ফাইল_পঢ়া  | file_poha  | read file           |
| ফাইল_লিখা | file_likha | write file          |
| http_লোৱা | http_lua   | fetch HTTP data     |

---

## Boolean and Logic Keywords

```ooju
ধৰা active = সঁচা
ধৰা empty = নাই

যদি active আৰু নহয় empty তেতিয়া:
    কোৱা "valid"
```

| Assamese | Romanized | Python |
| -------- | --------- | ------ |
| সঁচা     | xosa     | True   |
| মিথা     | misa     | False  |
| নাই      | nai       | None   |
| আৰু      | aru       | and    |
| নহলে     | nahole    | or     |
| নহয়     | nohoi     | not    |

---

## Error Handling in Ooju Programs

Ooju supports try-catch-finally style error handling.

```ooju
ট্ৰাই:
    কোৱা risky_value
ধৰা ভুল হলে:
    কোৱা "কিবা ভুল হৈছে"
শেষ:
    কোৱা "done"
```

Romanized:

```ooju
try:
    kua risky_value
dhora bhul hole:
    kua "something went wrong"
xekh:
    kua "done"
```

Generated Python:

```python
try:
    print(risky_value)
except Exception as bhul:
    print("something went wrong")
finally:
    print("done")
```

---

## Ooju Error Messages

Ooju includes beginner-friendly error messages for syntax, parse, and runtime issues.

### Syntax / transpile error

Example invalid code:

```ooju
ধৰা x
```

Output:

```txt
oi! bhul ase:
  file    : examples/test.oj
  line    : 1
  code    : ধৰা x
  kiba nai: 'dhora x' ৰ পিছত '=' lage
```

---

### Multiple syntax errors

The `check` command can collect multiple parser errors.

```bash
ooju check examples/test.oj
```

Example output:

```txt
oi! 2ta bhul ase:

  [1] line 1: 'dhora x' ৰ পিছত '=' lage
      code: ধৰা x

  [2] line 3: condition ৰ শেষত ':' লাগে
      code: যদি x > 5 তেতিয়া

Aarey dada!, 2ta bhul ase thik kora! 💪
```

---

### Tokenizer error

If Ooju finds a character it does not understand:

```txt
oi! bhul ase:
  file    : examples/test.oj
  line    : 2
  code    : ধৰা x = @
  kiba nai: ei character ta Ooju-t nai: '@'

Arey bhai!, Line 2-t eitu ki likhisa? Bhal ke sua!
```

---

### Runtime error with Ooju line mapping

Ooju maps runtime errors back to the original `.oj` line where possible.

Example invalid runtime code:

```ooju
ধৰা x = 10 / 0
কোৱা x
```

Output:

```txt
oi! runtime bhul (Ooju line 1):
  kiba nai: division by zero
```

---

## Imports

```ooju
অনা "utils.oj"
```

Romanized:

```ooju
ona "utils.oj"
```

---

## How Ooju Works Internally

Ooju uses a compiler-like pipeline:

```txt
Source Code
   ↓
Tokenizer
   ↓
Parser
   ↓
AST Nodes
   ↓
Code Generator
   ↓
Python Code
```

The tokenizer converts Assamese and romanized keywords into internal tokens. The parser builds AST nodes for assignments, functions, loops, lists, dictionaries, try-catch, imports, and more. The code generator then emits Python code and keeps a source map so runtime errors can point back to Ooju line numbers.

---

## Project Structure

```txt
Ooju/
├── ooju/
│   ├── core/
│   │   ├── tokenizer.py
│   │   ├── parser.py
│   │   ├── codegen.py
│   │   ├── transpiler.py
│   │   └── stdlib.py
│   └── cli/
│       ├── main.py
│       └── repl.py
├── examples/
├── tests/
├── editors/
│   └── vscode/
├── assets/
│   └── logo.png
└── README.md
```

---

## Example Program

```ooju
ধৰা নাম = লোৱা("তোমাৰ নাম কি? ")

কাম greet(person):
    যদি person == "Prabal" তেতিয়া:
        ঘুৰা "Welcome boss!"
    নহলে বা:
        ঘুৰা "Hello " + person

কোৱা greet(নাম)
```

---

## Roadmap

* [x] Assamese-inspired syntax
* [x] Romanized syntax support
* [x] Assamese script keyword support
* [x] Tokenizer
* [x] Parser
* [x] AST-based code generation
* [x] Source maps for runtime errors
* [x] CLI runner
* [x] Compile command
* [x] Syntax check command
* [x] Debug mode
* [x] REPL
* [x] Functions
* [x] Conditions
* [x] Loops
* [x] Lists and dictionaries
* [x] String helpers
* [x] Math helpers
* [x] Standard library helpers
* [x] Error handling
* [x] Import system
* [x] Multiple block styles
* [ ] More Assamese-first error messages
* [ ] Package publishing
* [ ] Documentation website
* [ ] More examples
* [ ] VS Code extension polish

---

## Contributing

Contributions are welcome.

You can help by:

* improving syntax
* adding examples
* improving error messages
* writing documentation
* adding tests
* improving the VS Code extension

---

## Philosophy

Ooju is not trying to replace Python, JavaScript, or C.

It is an experiment in making programming feel more natural for Assamese speakers and beginners.

The goal is simple:

> Make code feel less foreign.

---

## Author

Built by **Prabal Gogoi**.

If you like the idea, consider giving the repo a star.
