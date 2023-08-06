import os


def get_sample_adocfile():
    with open(os.path.join(os.path.realpath("."), "slide.adoc")) as fd:
        return fd.read()
