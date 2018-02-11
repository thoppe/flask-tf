from fabric.api import local


def test():
    local("nosetests tests -s --nologcapture")

def check():
    local("flake8 flasktf tests")
    local("nosetests tests -s --nologcapture --with-coverage "
          "--cover-package flasktf")

def lint():
    local("autopep8 tests flasktf -aaa --in-place --verbose -j 0 --recursive")
