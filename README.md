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
# Windows (PowerShell)
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
To see how to generate this custom config file and/or add a password see `Additional configuration` section below. 

**Launch Jupyter lab with an .env file**

To provide an .env file to the Jupyter environment, first create a .env file and place it in the repo (e.g. at the repo root)

You can add environment variables inside (e.g. DataJoint credentials) as follows:

```bash
DJ_HOST=at-database.stanford.edu
DJ_USER=...
DJ_PASS=...
```

To launch jupyter lab with the .env reflected in the environment, add `--env-file <path-to-env>` to any of the commands above. 

E.g.
```bash
uv run --env-file .env jupyter lab
```

or

```bash
uv run --env-file .env jupyter lab --config .jupyter/jupyter_server_config.py 
```

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

### Editable Install

To make code changes under `src/` immediately importable (e.g., inside Jupyter or VS Code), install the package in editable mode:

After `uv sync --frozen` has created a `.venv/` in this repo:

```bash
# Linux, macOS, or WSL, Windows
uv pip install -e .
```

This is one-time per environment (redo only if you recreate/delete the venv).

It works when the project’s virtual environment is the default `.venv/` inside the repo.

If the virtual environment lives **outside** the repo, install editable by pointing to that environment’s Python interpreter:

```bash
# Linux, macOS, or WSL, Windows
uv pip install --python "$(uv run python -c 'import sys; print(sys.executable)')" -e .
```

```powershell
# Windows (PowerShell)
uv pip install --python "$(uv run python -c \"import sys; print(sys.executable)\")" -e .
```

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

Some shared or remote filesystems (notably CIFS/SMB mounts) do not allow symbolic links, which `uv` uses
to link its managed Python interpreter into the project’s virtual environment.
If you see an error such as:    

```
error: failed to symlink file ... Operation not supported (os error 95)
```

#### Option 1:
Create the environment in a local path instead:

```bash
# Linux, macOS, or WSL
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/mouse-neuropixel-export"
uv sync --frozen
```
```powershell
# Windows (PowerShell)
$env:UV_PROJECT_ENVIRONMENT = "$HOME\.venvs\mouse-neuropixel-export"
uv sync --frozen
```

Your project code can still reside on the shared mount. 

If you want an editable install, after running the `uv sync` command above, run:

```bash
# Linux, macOS, or WSL, Windows
uv pip install --python "$(uv run python -c 'import sys; print(sys.executable)')" -e .
```

```powershell
# Windows (PowerShell)
uv pip install --python "$(uv run python -c \"import sys; print(sys.executable)\")" -e .
```
#### Option 2:

Enable symlinks on CIFS/SMB mounts (Linux only)

On some Linux systems, CIFS/SMB mounts can be configured to emulate symbolic links using the mfsymlinks mount option. If enabled, this allows uv to create the project’s .venv/ directly inside the repository, avoiding the need for an external virtual environment.

This is a client-side configuration and typically requires modifying /etc/fstab. For example:

```bash
//server/share  /mnt/lab  cifs  credentials=/path/to/creds,uid=1000,gid=1000,mfsymlinks  0  0
```
After updating fstab, remount the filesystem.

If this succeeds, uv sync --frozen should be able to create .venv/ in the repository as usual.
---

#### Note on system dependencies:
Some optional functionality (e.g. DataJoint schema diagram rendering) relies on external system tools that are not installed via Python package managers such as uv or pip. In particular, diagram rendering requires the Graphviz dot executable to be available on the system PATH. If this dependency is missing, related features may fail with a "dot" not found in path error. Installing Graphviz via your operating system’s package manager typically resolves the issue.

## References

* [`uv` documentation](https://docs.astral.sh/uv)
* [Jupyter Server configuration](https://jupyter-server.readthedocs.io/en/latest/users/configuration.html)

---

© 2025 Tolias Lab. MIT License.
