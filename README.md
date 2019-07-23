# HumanFramework: Test Automation Framework for Humans™

HumanFramework is a test automation framework that uses Natural Language Understanding (NLU).
It currently depend on [Microsoft LUIS (Language Understanding)](https://www.luis.ai/) for Intent Classification.

HumanFramework makes writing test cases easier by letting testers write test cases without the hassle of memorizing
any programming keyword and using the language they are comfortable with - the human language.

LUIS (and other NLU software) makes it easier to write tests on any written language.

In a business setup, HumanFramework lessens the need for testers who can write programs, reducing technical requirements.

## Usage

### Installing dependencies

HumanFramework is written in Python. Download from https://python.org and install dependencies using the following command:

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

## References

- [Simple Python Plugin Manager](https://gist.github.com/mepcotterell/6004997)
