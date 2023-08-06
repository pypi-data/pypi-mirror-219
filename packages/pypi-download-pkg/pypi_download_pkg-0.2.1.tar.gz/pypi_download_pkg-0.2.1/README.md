# CLI for Downloading packages for Linux

This is used in some build where we want to download all linux files for a package to avoid issues with azure functions or other environments where you don't really know the underlying system.

Usage: `download_linux_pkg --pkg-filter certifi --output-dir out`

You do need either a requirements.txt file or use poetry with poetry beeing available in PATH. In the later case we're generating requirements.txt on the fly

## Installation

`pip install pypi-download-pkg` 

See also https://pypi.org/project/pypi-download-pkg/
