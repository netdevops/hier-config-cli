# Installation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Installation Methods

### Via pip (Recommended)

The easiest way to install hier-config-cli is using pip:

```bash
pip install hier-config-cli
```

### Via Poetry

If you're using Poetry for dependency management:

```bash
poetry add hier-config-cli
```

### From Source

For development or to get the latest unreleased features:

```bash
# Clone the repository
git clone https://github.com/netdevops/hier-config-cli.git
cd hier-config-cli

# Install with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Verify Installation

After installation, verify that hier-config-cli is installed correctly:

```bash
# Check version
hier-config-cli version

# List available platforms
hier-config-cli list-platforms
```

You should see output similar to:

```
hier-config-cli version 0.2.0
```

## Updating

### With pip

```bash
pip install --upgrade hier-config-cli
```

### With Poetry

```bash
poetry update hier-config-cli
```

## Uninstalling

### With pip

```bash
pip uninstall hier-config-cli
```

### With Poetry

```bash
poetry remove hier-config-cli
```

## Troubleshooting

### Command Not Found

If you get a "command not found" error after installation:

1. **Check if the package is installed:**
   ```bash
   pip show hier-config-cli
   ```

2. **Ensure pip's bin directory is in your PATH:**
   ```bash
   # On Linux/macOS
   export PATH="$HOME/.local/bin:$PATH"

   # On Windows (PowerShell)
   $env:Path += ";$HOME\AppData\Local\Programs\Python\Python310\Scripts"
   ```

3. **Try running with python -m:**
   ```bash
   python -m hier_config_cli version
   ```

### Permission Errors

If you encounter permission errors during installation:

```bash
# Use --user flag to install in user directory
pip install --user hier-config-cli
```

### Virtual Environments

It's recommended to use virtual environments to avoid conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install hier-config-cli
pip install hier-config-cli
```

## Next Steps

Now that you have hier-config-cli installed, check out the [Quick Start](quick-start.md) guide to learn how to use it.
