from fabric.api import local

def test():
    local("nosetests tests -s --nologcapture")
    #local("flake8 nlpre --builtins basestring")
    #local("nosetests --with-coverage --cover-package nlpre --cover-html")
