<div align="center">

<img src="assets/ooju-logo.png" alt="Ooju logo — Bengali উজু in a glass sphere" width="220" />

# Ooju · উজু

**প্রোগ্রামিং এবাৰ অসমীয়াত!**

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen?style=flat-square)](https://github.com/Prabaaal/Ooju/releases)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-success?style=flat-square)](#)

> *ক'ডিং সদায়ে সহজ — তোমাৰ মাতৃভাষাত!*

</div>

---

## 🌟 কিয় Ooju?

তুমি কি কি পাৰে:
- 🗣️ **অসমীয়াত ক'ড লিখা** — ভাইটা ভাষাতে!
- ⚡ **Python য়ে চলে** — অতিৰিক্ত ৰানটাইম নাই
- 🛠️ **CLI টুলচ** — `run`, `compile`, `repl`, `version`
- 🔒 **সুৰক্ষিত** — sandboxed builtins, কোনো বিপদ নাই
- 🎨 **VS Code সাপোর্ট** — `.oj` ফাইলৰ বাবে syntax highlighting
- 📚 **শিকোৱা-বন্ধুত্বপূর্ণ** — স্পষ্ট, সহায়ক error messages

---

## 📦 ইনস্টলেশন

```bash
pip install ooju
```

### ডেভেলপমেন্ট ছেটআপ

```bash
git clone https://github.com/Prabaaal/Ooju.git
cd Ooju
pip install -e .
```

---

## 🚀 চালু কৰোৱা

`hello.oj` নামে এটা ফাইল তৈয়াৰ কৰা:

```
kaam greet(name):
    kua("নমস্কাৰ, " + name)

dhora naam = lobo("তোমাৰ নাম কি? ")
greet(naam)
```

চলাওঁ:

```bash
ooju run hello.oj
```

সৃষ্টি হোৱা Python দেখা:

```bash
ooju run hello.oj --debug
```

`.py` ফাইললৈ কম্পাইল কৰা:

```bash
ooju compile hello.oj
```

---

## 📖 ভাষা গাইড

### চলক (Variables)
```
dhora x = 5
dhora greet = "নমস্কাৰ!"
```

### আউটপুট & ইনপুট
```
kua("নমস্কাৰ!")          # print
dhora name = lobo("কি?")  # input
```

### ফাংশন
```
kaam add(a, b):
    return a + b
```

### চর্ত (Conditionals)
```
jodi (x > 5) hoi, tetia:
    kua("বেছি")
nohole jodi (x > 3) hoi, tetia:
    kua("মধ্যম")
nohole ba:
    kua("কম")
```

### লুপ
```
# N সময় দোহাৰা
3 bar kora:
    kua("hello")

# While লুপ
jetialoike (x < 10) bare bare kora:
    dhora x = x + 1
```

### মন্তব্য
```
// এইটো এক লাইন মন্তব্য

///
এইটো এটা
ব্লক মন্তব্য
///
```

---

## ⚠️ ত্রুটি বার্তা

Ooju-য় শিকনৰ্থী-বন্ধুত্বপূর্ণ errors দিয়ে:

```
OojuError:
  File : hello.oj
  Line : 3
  Code : dhora naam
  Issue: 'dhora' ৰ পাছত এসাইনমেন্ট নাই
  Help : ভুলবশতঃ: dhora x = 10 ?
```

---

## 📂 প্ৰজেক্ট স্ট্রাকচাৰ

```
Ooju/
├── assets/             # ব্র্যান্ডিং (logo)
├── ooju/               # মূল ভাষা প্যাকেজ
│   ├── tokenizer.py    # Lexer — text → tokens
│   ├── parser.py       # Parser — tokens → AST
│   ├── codegen.py      # Code generator — AST → Python
│   ├── transpiler.py   # Pipeline orchestrator
│   ├── cli.py          # কমান্ড-লাইন ইণ্টাৰফেচ
│   ├── repl.py         # ইণ্টাৰেক্টিভ REPL
│   └── stdlib.py       # সুৰক্ষিত builtins sandbox
├── examples/           # নমুনা .oj প্ৰগ্রাম
├── tests/              # Pytest test suite
├── editors/vscode/     # VS Code syntax extension
├── pyproject.toml
└── README.md
```

---

## 🧪 টেস্ট চলোৱা

```bash
pip install pytest
pytest tests/
```

---

## 🎨 সম্পাদক সাপোর্ট

`.oj` ফাইলৰ বাবে syntax highlighting **VS Code**-ত পোৱা যায়।

```bash
cd editors/vscode
npm install
npm run package          # builds the .vsix
code --install-extension ooju-vscode-*.vsix
```

---

## 🤝 অবদান

অবদান আমোদজনক! এভাবে আৰম্ভ কৰা:

1. Fork the repo
2. ফিচাৰ ব্রাঞ্চ তৈয়াৰ কৰা: `git checkout -b feature/your-feature`
3. পৰিবৰ্তন commit কৰা: `git commit -m "feat: add your feature"`
4. Push কৰা আৰু Pull Request খোলা

অনুগ্রহ কৰা সকলো টেস্ট পাছ হোৱাৰ আগতে submit কৰা।

---

## 📄 লাইসেন্স

MIT © [Prabal Gogoi](https://github.com/Prabaaal)

---

<div align="center">

❤️ অসমীয়া শিকনৰ্থীৰ বাবে তৈয়াৰ

*ক'ডিং এবাৰ — অসমীয়াত!*

</div>