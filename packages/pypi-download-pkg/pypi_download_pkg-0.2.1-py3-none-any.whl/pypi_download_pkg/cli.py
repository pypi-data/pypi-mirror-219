import os
import re
from typing import List, Optional
import requests

def get_deps(req_file: str):
    
    def parse_file(f):
        l = f.readline()
        while l is not None and l != "":
            if l and not l.strip().startswith("--"):
                pkg, version = l.split(";")[0].split("==")
                if "[" in pkg:
                    pkg = pkg[0 : pkg.index("[")]
                yield pkg, version.strip()
            l = f.readline()

    if req_file == "auto":
        if os.path.exists("requirements.txt"):
            req_file ="requirements.txt"
        else:
            import subprocess
            import io
            output = subprocess.run("poetry export -f requirements.txt --without-urls --without-hashes", stdout=subprocess.PIPE).stdout.decode("utf-8")
            with io.StringIO(output) as iof:
                for i in parse_file(iof):
                    yield i
    else:
        with open(req_file, mode="r") as f:
            for i in parse_file(f):
                yield i

linux_regexes = [
            re.compile("manylinux.*[_]aarch64[.]whl"),
            re.compile("manylinux.*[_]x86[_]64[.]whl"),
            re.compile("manylinux.*[_]i686[.]whl"),
            re.compile("musllinux.*[_]aarch64[.]whl"),
            re.compile("musllinux.*[_]x86[_]64[.]whl"),
            re.compile("musllinux.*[_]i686[.]whl"),
        ]

def is_linux(filename: str):
    return any((r for r in linux_regexes if re.search(r, filename)))

def handle_package(pk: str, version: str, output_dir: str):
    url = f"https://pypi.org/pypi/{pk}/json"
    r = requests.get(url)
    r.raise_for_status()
    releases = r.json()["releases"]
    for pkg_version, pkg_files in releases.items():
        if pkg_version == version:
            for fl in pkg_files:
                if (
                    fl["packagetype"] == "sdist"
                    or fl["filename"].endswith("-none-any.whl")
                    or is_linux(fl["filename"])
                ):
                    if not os.path.exists(os.path.join(output_dir, fl["filename"])):
                        download_url = fl["url"]
                        r = requests.get(download_url, stream=True)
                        r.raise_for_status()
                        os.makedirs(output_dir, exist_ok=True)
                        with open(os.path.join(output_dir, fl["filename"]), 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        print("do " + fl["filename"])
                    else:
                        print("already done " + fl["filename"])
                elif (
                    "-macosx_" in fl["filename"]
                    or "ppc64le." in fl["filename"]
                    or fl["filename"].endswith("s390x.whl")
                    or fl["filename"].endswith("win32.whl")
                    or fl["filename"].endswith("win_amd64.whl")
                    or fl["filename"].endswith("win_arm64.whl")
                    or fl["filename"].endswith("win_arm32.whl")
                    or fl["filename"].endswith("armv7l.whl")
                    or re.search("armv[0-9]*[a-z]{0,3}.whl", fl["filename"])
                ):
                    print("ignoring " + fl["filename"])
                else:
                    print("not sure about " + fl["filename"] + ". Ignoring for now")
                    print(fl["packagetype"])

def execute(req_file: str, pkg_filter: Optional[List[str]], output_dir: str):
    if pkg_filter and len(pkg_filter) == 0:
        pkg_filter = None

    done_any = False
    all_deps = []
    for pkg, version in get_deps(req_file):
        all_deps.append(pkg)
        if pkg_filter and not pkg in pkg_filter:
            continue
        done_any = True
        handle_package(pkg, version, output_dir)
    if not done_any and pkg_filter is not None:
        print("Could not find package: " + ", " .join(pkg_filter))
        print("Can be any of : " + ", ".join(all_deps))


def cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pkg-filter", nargs="+")
    parser.add_argument("--output-dir", default="_dependencies")
    parser.add_argument("-r", "--requirements-file", default="auto")
    args = parser.parse_args()
    execute(args.requirements_file, args.pkg_filter, args.output_dir)
if __name__ == "__main__":
    cli()
