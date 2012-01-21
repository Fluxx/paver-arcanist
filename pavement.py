import os
import sys

sys.path.insert(0, os.path.abspath("."))

from paver.easy import *
from util import *

phabricator = path('/usr/local/phabricator')
bins = path('/usr/local/bin')
root = path(os.path.abspath("."))

@task
def install(options):
    """
    Install Arcanist onto your system
    """

    mkdir(phabricator)

    update()

    # Symlink arc to the bins
    if not path.exists(bins / 'arc'):
        (phabricator / 'arcanist' / 'bin' / 'arc').symlink(bins / 'arc')

    # Build xphast
    sh(phabricator / 'libphutil' / 'scripts' / 'build_xhpast.sh')


@task
def update(options):
    # Install or update libphutil
    git.clone_or_update('git://github.com/facebook/libphutil.git', phabricator / 'libphutil')

    # Install or update arcanist
    git.clone_or_update('git://github.com/facebook/arcanist.git', phabricator / 'arcanist')

    # Install or update phabricator
    git.clone_or_update('git://github.com/facebook/phabricator.git', phabricator / 'phabricator')

    # Install or update libdisqus
    git.clone_or_update('git@github.com:disqus/disqus-arcanist.git', phabricator / 'libdisqus')

@task
@cmdopts([
    ('immutable', 'i', 'Use immutable history'),
    ('directory=', 'd', 'Directory to init into'),
    ('template=', 't', 'Directory to init into.  Defaults to /install/directory/.arcconfig.tmpl')
])
def init(options):
    """
    Initializes Arcanist into a directory and writes a .arcconfig file there.
    """

    libdisqus = phabricator / 'libdisqus' / 'src'
    destination_folder = path(options.directory)
    destination_arcconfig = destination_folder / '.arcconfig'

    if options.get('template'):
        template = path(options.template)
    else:
        template = path(os.environ['HOME']) / '.arcconfig.tmpl'

    if not template.exists():
        raise Exception("Template '%s' not found" % template)
    else:
        print "Using .arcconfig template: %s" % template

    os.chdir(destination_folder)

    if options.get('immutable'):
        git.config('--unset branch.autosetuprebase', ignore_error=True)
        git.config('--unset commit.template', ignore_error=True)
        sed('"immutable_history": false', '"immutable_history": true', destination_arcconfig)
    else:
        git.config(
            'commit.template %s' % (
                phabricator / 'arcanist' / 'resources' / 'git' / 'commit-template.txt'
            )
        )
        git.config('branch.autosetuprebase always')
        sed('"immutable_history": true', '"immutable_history": false', destination_arcconfig)
