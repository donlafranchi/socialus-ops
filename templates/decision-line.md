# A decision line

One dated line per live ruling, newest first, in the project's `DECISIONS.md`:

```
- **YYYY-MM-DD — The ruling, in one sentence a newcomer can act on.** Who ruled, and their words if they gave them. What it restates or builds on. [replaces YYYY-MM-DD: exact old text] [binds tiers=planning,code surfaces=a,b #N]
```

- `[replaces …]` only when it supersedes something; the superseded text is deleted in the same commit. Also `[replaces F###: old text]`, `[replaces path.md]`, or `[replaces none]` when a word like "replaces" is not a supersession.
- `[binds …]` on every line: `tiers=planning,code` or `tiers=none`. A line binding `code` names its Issue (`#N`), its scenario (`F###`), or `build=none`.
- Then run `python3 scripts/markers.py constraints`; the lint fails until you do.
