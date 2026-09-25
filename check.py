#!/usr/bin/env python3
"""Checks disposable.txt and exclude.txt the way ca-web reads them.

CI runs this on every pull request; run `python3 check.py` locally before pushing.
"""
import os
import re
import sys
from pathlib import Path

# Never block these, nor anything they sit under: ca-web also matches every parent domain of an
# address, so an entry of co.uk would block hotmail.co.uk. Extend the list freely.
NEVER = """
    gmail.com googlemail.com outlook.com hotmail.com hotmail.co.uk hotmail.com.br live.com msn.com
    yahoo.com yahoo.co.uk yahoo.co.jp yahoo.com.br ymail.com icloud.com me.com mac.com aol.com
    proton.me protonmail.com pm.me tutanota.com gmx.com gmx.de gmx.net web.de t-online.de
    mail.ru yandex.ru yandex.com zoho.com fastmail.com qq.com 163.com 126.com naver.com
    seznam.cz wp.pl libero.it orange.fr free.fr bigpond.com.au btinternet.com comcast.net
    convertapi.com
""".split()

DOMAIN = re.compile(r"([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+([a-z]{2,63}|xn--[a-z0-9-]+)")

errors = 0


def error(file, line, message):
    global errors
    errors += 1
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::error file={file},line={line}::{message}")
    else:
        print(f"{file}:{line}: {message}")


def entries(file):
    """(line number, domain) per entry, read as ca-web's DisposableDomainList.Parse reads it:
    blank lines and lines starting with # or // are skipped, and the domain is the first word."""
    for number, text in enumerate(Path(file).read_text(encoding="utf-8").splitlines(), 1):
        text = text.strip()
        if text and not text.startswith(("#", "//")):
            yield number, text.split()[0]


os.chdir(Path(__file__).parent)

lists = {}
for file in ("disposable.txt", "exclude.txt"):
    lists[file] = {}
    for line, domain in entries(file):
        if not DOMAIN.fullmatch(domain):
            error(file, line, f"'{domain}' is not a lower-case domain name")
        elif domain in lists[file]:
            error(file, line, f"{domain} is already on line {lists[file][domain]}")
        else:
            lists[file][domain] = line

excluded = lists["exclude.txt"]
for domain, line in lists["disposable.txt"].items():
    if domain in excluded:
        error("disposable.txt", line, f"{domain} is also in exclude.txt, line {excluded[domain]}")
    blocked = next((n for n in NEVER if n == domain or n.endswith("." + domain)), None)
    if blocked:
        error("disposable.txt", line, f"{domain} would block {blocked}")

if errors:
    sys.exit(f"{errors} problem(s) found")
print(f"OK: {len(lists['disposable.txt'])} disposable, {len(excluded)} excluded")
