## Bastila

### Installation Instructions

1. Install the package `pip install bastila-search`
2. Create a precommit file `touch .git/hooks/pre-commit`
3. Add execute access to that file `chmod +x .git/hooks/pre-commit`
4. Add the script to your pre-commit file

```
#!/bin/sh
bastila_run
```