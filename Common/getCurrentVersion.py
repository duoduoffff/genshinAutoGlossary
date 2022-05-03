#! /usr/local/bin/python3

# https://stackoverflow.com/questions/7293008/display-last-git-commit-comment
# https://stackoverflow.com/questions/7622616/executing-a-git-pull-from-a-different-directory
# https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script

import subprocess

from Common import conf

def get():
    dir = conf.dataPath
    print(dir)
    return subprocess.check_output(['git', '-C', '{0}'.format(dir), 'log', '--grep=OSREL', '-1', '--pretty=%B']).decode('ascii').strip()

if __name__ == '__main__':
    print(get())