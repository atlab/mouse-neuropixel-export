from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mouse-neuropixel-export")
except PackageNotFoundError:
    __version__ = "0+unknown"
