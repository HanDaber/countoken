#!/usr/bin/env -S uv run --script
# /// script
# name = "countoken"
# version = "0.0.1"
# description = "Wrapper for ttok"
# requires-python = ">=3.9"
# ///

import os
import shutil
import sys
import stat
import filecmp


def get_user_bin_dir():
    if os.name == "nt":  # Windows
        # Prefer Scripts in user Python install, fallback to APPDATA
        scripts_dir = os.path.join(sys.prefix, 'Scripts')
        if os.path.isdir(scripts_dir):
            return scripts_dir
        appdata = os.environ.get('APPDATA')
        if appdata:
            return os.path.join(appdata, 'Python', 'Scripts')
        # Fallback: user home
        return os.path.expanduser('~')
    else:
        # Linux/macOS
        return os.path.expanduser("~/.local/bin")


def is_same_file(src, dst):
    try:
        return os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False)
    except Exception:
        return False


def make_executable(path):
    if os.name != "nt":
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)


def main():
    src = os.path.abspath("countoken")
    bindir = get_user_bin_dir()
    os.makedirs(bindir, exist_ok=True)
    dst = os.path.join(bindir, "countoken")

    if is_same_file(src, dst):
        print(f"countoken is already installed and up-to-date at {dst}")
        return

    try:
        shutil.copy2(src, dst)
        make_executable(dst)
        print(f"Installed countoken to {dst}")
    except Exception as e:
        print(f"Failed to install: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()