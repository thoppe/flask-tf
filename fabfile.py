from fabric.api import local


def test():
    local("flake8 flasktf")
    local("nosetests tests -s --nologcapture --with-coverage "
          "--cover-package flasktf")
    # local("nosetests --with-coverage --cover-package nlpre --cover-html")


def lint():
    local("autopep8 flasktf -aaa --in-place --verbose -j 0 --recursive")
