"""
Generates information for meta.yaml file
"""

import os
import re
import sys
import subprocess
import traceback
from time import sleep
from pathlib import Path

import requests

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

print('We should check if PyPi is ready with our newest version')
max_retries = 3
sleepinbetween = 20  # seconds
url = 'https://pypi.org/project/{}/{}/'.format(
    reponame.replace('_', '-'), version)
tries = 0
while True:
    res = requests.get(url)

    if res.status_code == 200:
        break

    tries += 1
    if tries >= max_retries:
        print("Couldn't find version in PyPi. URL: {}".format(url),
              file=sys.stderr)
        sys.exit(1)
    print('Try #{} did not find suitable version'.format(tries))
    sleep(sleepinbetween)

# if managed to survive up until here then there is an updated version in PyPi
# if grayskull is available, use it instead of our own solution here
nograyskull = False
pathout = '{}/meta.yaml'.format(reponame)
pathold = pathout + '.old'
thereisanoldone = False
if os.path.isfile(pathout):  # check if output file of grayskull already exists
    # is does, so move it to somewherelse
    os.replace(pathout, pathold)
    thereisanoldone = True

res = subprocess.run(['grayskull', 'pypi', reponame], stdout=subprocess.PIPE)
try:
    res.check_returncode()
    # move the generated file to output
    os.replace(pathout, output)
    if thereisanoldone and pathold != pathout:
        os.replace(pathold, pathout)
        os.remove(pathout)
except subprocess.CalledProcessError:
    nograyskull = True
    traceback.print_exc()
    print('\nWe found error with grayskull. Trying different method')

# reads requirements from setup.cfg to update the meta.yaml file
# (even though it wont be used)
if nograyskull and not use_py:  # if it uses .cfg
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
