## Bastila

[Bastila](https://bastila.app/) is a tool for removing deprecated code. You define deprecated patterns using regex in the app and then prevent additional usages of those deprecated patterns from being used. The tool can also be used to track the removal of these patterns as well.

### Installation Instructions

1. Install the package `pip install bastila-search`
2. Create a precommit file `touch .git/hooks/pre-commit`
3. Add execute access to that file `chmod +x .git/hooks/pre-commit`
4. Add the script to your pre-commit file
```
#!/bin/sh
bastila_run
```
5. Run the setup command to create a config file with your env vars `bastila_setup`. This will create a config.json file that should be kept in the root of your repository.

Support: hello@bastila.app
