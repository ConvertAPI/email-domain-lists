# E-mail domain lists

ConvertAPI checks sign-up addresses against public disposable e-mail lists. These two files are its own corrections to them:

| File | Holds | Effect |
|---|---|---|
| [`disposable.txt`](disposable.txt) | disposable domains the public lists miss | sign-ups from them get no verification code |
| [`exclude.txt`](exclude.txt) | legitimate domains a public list gets wrong | removed from the block list, so sign-ups go through |

## How they are used

The ConvertAPI website downloads both files alongside the public lists:

- `https://raw.githubusercontent.com/ConvertAPI/email-domain-lists/main/disposable.txt`
- `https://raw.githubusercontent.com/ConvertAPI/email-domain-lists/main/exclude.txt`

It refreshes them every hour, so a merged change goes live within about an hour without a website release. If a download fails, it keeps the last copy it had.

- **Blocking also covers subdomains:** an entry `example.com` also blocks `x@mail.example.com`.
- **An exclusion removes that exact domain only:** excluding `example.com` does not unblock `temp.example.com` if that is listed itself.

## Format

One domain per line, lower case, no `@`. A note can follow the domain after a space. Lines starting with `#` are comments.

```
raxio.app        # temp-mail.id, reported 2026-09-25
```

## Changing a list

- **Domains only.** Never commit an e-mail address, a name or anything else about a person.
- **Changes go through a pull request into `main`.** Direct pushes are blocked, but no approval or checks are needed, so whoever merges is responsible for the entry.
- **Never add a large provider or a shared suffix to `disposable.txt`.** An entry also blocks every domain under it, so `co.uk` would block `hotmail.co.uk`.
- **For `disposable.txt`**, say in the pull request why the domain is disposable, for example a temp-mail site offering it or a checker such as UserCheck. Consider reporting it to the public lists too.
- **For `exclude.txt`**, say which public list has it wrong and why the domain is legitimate. Reporting it to that list gets it fixed at the source.
