# Human Framework: Test Automation Framework for Humans™

Human Framework is a test automation framework that uses Natural Language Understanding (NLU).
It currently depend on [Microsoft LUIS (Language Understanding)](https://www.luis.ai/) for Intent Classification.

Human Framework makes writing test cases easier by letting testers write test cases without the hassle of memorizing
any programming keyword and using the language they are comfortable with - the human language.

LUIS (and other NLU software) makes it possible to write test cases on any written language. 
Current version only support English. 

In a business setup, Human Framework lessens the need for testers who can write programs, reducing technical requirements.

Human Framework was inspired by [Robot Framework](https://robotframework.org/) but leans towards 
Natural Language Processing (NLP) for writing test cases.

## Usage

### Installation

Human Framework is written in Python. 
Start by downloading Python from [python.org](https://python.org) and install using the following command:

```bash
python setup.py sdist
pip install dist/humanframework-<version>.tar.gz
```

### Writing tests

Write a text file (.txt) containing your tests. For example, if we have a file named "test_web.txt":

```text
open chrome https://python.org
page title should be "Welcome to Python.org"
close browser
```

### Running tests

```bash
human --test test_web.txt
```

## Author

- [Ronie Martinez](mailto:ronmarti18@gmail.com)
