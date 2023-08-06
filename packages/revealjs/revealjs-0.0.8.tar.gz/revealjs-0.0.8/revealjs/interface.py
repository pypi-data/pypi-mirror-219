import os


def get_sample_adocfile():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(script_dir, "slide.adoc")) as fd:
        return fd.read()
