# Human Framework: Test Automation Framework for Humans™

Human Framework is a test automation framework that uses Natural Language Understanding (NLU).
It currently depend on [Microsoft LUIS (Language Understanding)](https://www.luis.ai/) for Intent Classification.

Human Framework makes writing test cases easier by letting testers write test cases without the hassle of memorizing
any programming keyword and using the language they are comfortable with - the human language.

LUIS (and other NLU software) makes it possible to write test cases on any written language. 
Current version only support English. 

In a business setup, Human Framework lessens the need for testers who can write programs, reducing technical requirements.

Human Framework is inspired by [Robot Framework](https://robotframework.org/) but leans towards 
Natural Language Processing for writing test cases.

## Usage

### Installing dependencies

Human Framework is written in Python. Download from https://python.org and install dependencies using the following command:

```bash
pip install -r requirements.txt
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
python human.py test test_web.txt
```

## Author

- [Ronie Martinez](mailto:ronmarti18@gmail.com)
