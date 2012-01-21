from paver.easy import sh
from path import path
from os import environ


def mkdir(path):
    sh('mkdir -p "{0}"'.format(path))


def wget(url, output_file):
    sh('curl -o {0} {1}'.format(output_file, url))


def sed(find, replace, file, into=False):
    format = "'s@%(find)s@%(replace)s@g' %(file)s"

    if into:
        format += " > %s" % into
    else:
        format = "-i bak " + format

    sh('sed ' + (format % locals()))


# we just use git as a fake namespace
class git:
    @classmethod
    def clone(cls, url, output_path):
        sh('git clone "{0}" "{1}"'.format(url, output_path))

    @classmethod
    def clone_or_update(cls, url, output_path):
        if (output_path / '.git').exists():
            cls.update(output_path)
        else:
            cls.clone(url, output_path)

    @classmethod
    def update(cls, output_path):
        sh('git pull -q', cwd=output_path)

    @classmethod
    def config(cls, rest, *args, **kwargs):
      sh('git config %s' % rest, *args, **kwargs)


class pip:
    @classmethod
    def install(cls, name_or_file, file=False):
        if file:
            sh('pip install -r {0}'.format(name_or_file))
        else:
            sh('pip install {0}'.format(name_or_file))
