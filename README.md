# pypirepoctrl

Helps control and maintain releases, pre-releases and PyPi packages.

## Requirements

- `hub` - check: https://github.com/github/hub

- `git` - check: https://git-scm.com/

- `python3` - check: https://www.python.org/

- `twine` - check: https://pypi.org/project/twine/

## Compatibility
This script is compatible with any Linux distribution with a bash script interpreter.

## Installation

Please follow the installation steps provided in each and every requirement for this script before attempting to install the content of this repository.

There is multiple ways to get this code, we cover two. The first one being the `git clone` of this repo, which implies that you will get the most updated version of this script (if there will ever be another update...). Please open a terminal, navigate to a safe directory and clone the repository.

```bash
cd my_safe_dir
git clone git@github.com:anewmanvs/pypirepoctrl.git
```

The second method is to download the source code from a release and unzip in a safe directory. You can find releases [here](https://github.com/anewmanvs/pypirepoctrl/releases).

While there is no explicit installation of this scripts, it is recommended to create a symbolic link to the actual bash script. This would make it easier to use in every day update and maintenance.

```bash
sudo ln -s $(pwd)/update_release /usr/local/bin/update_release
```

After that, you can use `update_release` as a regular native command.

### Auth

You still have to provide credentials to push to GitHub and PyPi. The script merely asks for those credentials, it does not store anything on its own. Be careful when working with credentials, specially if it is a file.

Specifically when dealing with `hub`, you need to setup an access token to grant you authentication. Please read [this doc](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) and follow to steps to setup your token. On the first usage, the script will prompt you for your username and password. Instead, you should put the token into the password field.

PyPi credentials must be stored to expedite package pushes. Be careful, you **must place the file with your credentials outside of the repository** for security matters. This script expects your credentials stored in `~/.pypirc`. If that's not the case, you should create with the following content:

```
[distutils]
index-servers =
    pypi
    pypitest

[pypi]
repository=https://upload.pypi.org/legacy/
username=__token__
password=[your token]

[pypitest]
repository=https://test.pypi.org/legacy/
username=__token__
password=[your token]
```

Please note that you are not going to use your explicit username and password to authenticate with PyPi. You must create an API Token with permissions to the package you're trying to upload. Refer to [this link](https://pypi.org/help/#apitoken) to learn how tokens work and how to create them. **Note that `pypitest` is a completely different domain with different usernames and tokens**.

Again, **do not post any of your credentials in a public repository**.

## Usage

```bash
./update_release dir (major | minor | patch) [-p] [-py]
```

First arg points the dir to operate over and is NOT-OPTIONAL. Second arg indicates the release type and is NOT-OPTIONAL. Third arg indicates if it is a pre-release and is OPTIONAL. Fourth arg is also OPTIONAL and if provided will work over `setup.py` instead of `setup.cfg`.	

## What does it do?

This script will calculate the new version number, commit the modifications to setup.py (may require your credentials in the process), push the `main` branch, add a new release in github and upload the package to PyPi.

This version number is calculated based on the [Semantic Versioning](https://semver.org/). A brief explanation would be a formation of three integers, each separated by a point, whereas they represent major, minor and patch version, respectively:

- MAJOR version when you make incompatible API changes;
- MINOR version when you add functionality in a backwards compatible manner;
- PATCH version when you make backwards compatible bug fixes.

If your current branch isn't `main`, you will have to merge to `main` before using this script. Your main branch must conform to latest github practices and be called `main` instead of previous `master` name. You can always change the script in `update_release` to fit your requirements, though.

