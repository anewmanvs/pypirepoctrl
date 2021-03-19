"""
Generates information for meta.yaml file
"""

import re
import sys
import subprocess
from pathlib import Path

source_path = Path(__file__).resolve()
source_dir = source_path.parent

params = sys.argv[1:]
tam = len(params)
if tam < 4 or tam > 5:
    print("Usage:\npython genmeta.py reponame tarball version output [-py]")

use_py = False
pyoption = '-py'

reponame = params[0]
tarball = params[1]
version = params[2]
output = params[3]
if pyoption in params[4:]:
    use_py = True

setupfilename = 'setup.{}'.format('py' if use_py else 'cfg')
metayamlfiletemp = '{}/{}'.format(source_dir, 'meta.yaml.template')

with open(metayamlfiletemp, 'r') as _f:
    metacontent = _f.read()

with open(setupfilename, 'r') as _f:
    content = _f.read().lower()

# reads requirements from setup.cfg to update the meta.yaml file
# (even though it wont be used)
if not use_py:  # if it uses .cfg
    pttn = re.compile(
        r'install_requires\s*=\s*((?:[0-9a-z\-_\s.]|[<>=]{2}|[><])+)\n')
    func = lambda x: '    - {}'.format(x.strip())

    # capture requirements
    requirements = '\n'.join(
        list(map(func, pttn.findall(content)[0].split('\n'))))
    # capture home
    home = re.findall(r'url\s*=\s*(.+)\n', content)[0]
    # capture summary
    summary = re.findall(r'description\s*=\s*(.+)\n', content)[0]

    # gets sha256 hash from recently pushed pypi package
    res = subprocess.run(['openssl', 'sha256', tarball],
                         stdout=subprocess.PIPE)
    _hash = re.findall(r'SHA256\(.+\)=\s+(.+)', res.stdout.decode('utf-8'))[0]

    # fills meta yaml template with actual data
    metacontent = metacontent.format(
        requirements, _hash, version, reponame, home, summary)

    with open(output, 'w') as _f:
        _f.write(metacontent)
