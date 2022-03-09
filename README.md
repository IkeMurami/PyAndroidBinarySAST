# About

В этом проекте присутствуют два класса-обертки для AndroGuard и LIEF:

- features/AndroGuard.py
- features/LIEF.py

По факту, сейчас через AndroGuard возвращается список классов, расширяющих класс `Lcom/google/protobuf/GeneratedMessageLite;`.
Это все классы, в которых определены типы данных для gRPC API.

PS: work slowly (~4 min)

# Pre-Install

```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -r requirements.txt
```

# Usage

```
python main.py -i my.apk -o classes.txt [--base 'Lcom/google/protobuf/GeneratedMessageLite;']
```