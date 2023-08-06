import pkg_resources


def get_sample_adocfile():
    file_path = pkg_resources.resource_filename("revealjs", "slide.adoc")

    with open(file_path, "r") as file:
        slide_contents = file.read()
        return slide_contents
