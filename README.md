# mouse-neuropixel-export

Export utilities and notebooks for Tolias Lab mouse Neuropixels data.
Built around a minimal, portable [`uv`](https://docs.astral.sh/uv) setup.

---

## Quick Start

### 1. Install `uv`

```bash
# Linux, macOS, or WSL
curl -Ls https://astral.sh/uv/install.sh | sh
exec $SHELL -l  # reload your shell
uv --version
```

```powershell
# Windows (Powershell)
irm https://astral.sh/uv/install.ps1 | iex
# open a new PowerShell window
uv --version
```

### 2. Clone the repository and navigate inside

```bash
# Linux, macOS, or WSL
git clone https://github.com/atlab/mouse-neuropixel-export.git
cd mouse-neuropixel-export
```

### 3. Sync the environment

```bash
uv sync --frozen
```

This will:

* Ensure a **Python** interpreter matching the version specified in the pyproject.toml
* Create a local virtual environment at `.venv/`
* Install dependencies defined in `pyproject.toml` and `uv.lock`

The `--frozen` flag ensures that dependencies are installed exactly as specified in `uv.lock`
(it will fail if the lockfile and pyproject.toml are out of sync).

### 4. Launch JupyterLab

**Option a. Without additional configuration:**

```bash
# Linux, macOS, or WSL, Windows
uv run jupyter lab
```

**Option b. Ad-hoc (override port, etc.):**

```bash
# Linux, macOS, or WSL, Windows
uv run jupyter lab --port 8890 --no-browser
```

**Option c. With a custom config file:**

```bash
# Linux, macOS, or WSL, Windows
uv run jupyter lab --config .jupyter/jupyter_server_config.py
```
To see how to generate this file and/or add a password see `Additional configuration` section below. 

### 5. Access JupyterLab

The terminal will display connection information, including the access URL for your JupyterLab session. Open that URL in a web browser (or use the configured hostname, port, and credentials if running remotely).

### 6. Alternatively, run Jupyter notebooks inside VS Code

1. Make sure you've run `uv sync --frozen`
2. Open a `.ipynb` Jupyter notebook
3. Select the kernel named `Python (mouse-neuropixel-export)` or similar
4. Run cells as usual.

VS Code will automatically use the environment created by `uv`.

---

## Additional Configuration

### Generate a Jupyter server config file

Create a repo-local Jupyter config.

#### 1. Create a directory called `.jupyter` at the repo root. (It is automatically ignored by .gitignore)

#### 2. Generate the file
```bash
# Linux, macOS, WSL
JUPYTER_CONFIG_DIR=./.jupyter jupyter server --generate-config
```
```powershell
# Windows Powershell
$env:JUPYTER_CONFIG_DIR = ".\.jupyter"
jupyter server --generate-config
Remove-Item Env:JUPYTER_CONFIG_DIR
```

Note: The generator won’t overwrite an existing file. Delete or rename an older config if you want a fresh template.

#### 3. Launch with custom config

```bash
# Linux, macOS, or WSL, Windows
uv run jupyter lab --config .jupyter/jupyter_server_config.py
```

### Authentication (set a password)

Set a password directly in the Python config file (`.jupyter/jupyter_server_config.py`)

#### 1. Generate a hashed password

```bash
# Linux, macOS, WSL, Windows
uv run python -c "from jupyter_server.auth import passwd; print(passwd())"
```

#### 2. Copy the printed string (it will start with `argon2`).

#### 3. Edit `.jupyter/jupyter_server_config.py` and include:

```python
c.PasswordIdentityProvider.hashed_password = <paste string here>
```
#### 4. Launch Jupyter with custom config:

```bash
# Linux, macOS, or WSL, Windows
uv run jupyter lab --config .jupyter/jupyter_server_config.py
```

---

## Known Issues

### Running on network or shared filesystems (e.g., `/mnt`, SMB, NFS, WSL mounts)

Some shared or remote filesystems do not allow symbolic links, which `uv` uses
to link its managed Python interpreter into the project’s virtual environment.
If you see an error such as:    

```
error: failed to symlink file ... Operation not supported (os error 95)
```

Create the environment in a local path instead:

```bash
# Linux, macOS, or WSL
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/mouse-neuropixel-export"
uv sync --frozen
```
```powershell
# Windows (Powershell)
$env:UV_PROJECT_ENVIRONMENT = "$HOME\.venvs\mouse-neuropixel-export"
uv sync --frozen
```

Your project code can still reside on the shared mount.

---

## References

* [`uv` documentation](https://docs.astral.sh/uv)
* [Jupyter Server configuration](https://jupyter-server.readthedocs.io/en/latest/users/configuration.html)

---

© 2025 Tolias Lab. MIT License.
