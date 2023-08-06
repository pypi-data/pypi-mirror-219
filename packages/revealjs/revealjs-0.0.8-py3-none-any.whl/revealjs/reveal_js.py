"""
Building the presentation using the reveal js .

command to build html page.
    - python3 build.py
        or 
    - make slide
"""


import sys
from subprocess import run
import os
import base64
from bs4 import BeautifulSoup
from requests import get
from inquirer import Text, List, prompt, themes
from .interface import get_sample_adocfile

DEFAULT_PLUGINS = ["markdown", "math", "notes", "highlight"]
VIDEO_FORMATS = ["mp4", "avi", "mkv", "mov", "wmv"]
AUDIO_FORMATS = ["mp3", "wav", "aac", "ogg", "flac"]

SOURCE_FILE_NAME = ""
PLUGINS = list(
    filter(
        lambda val: val.strip(),
        "highlight  markdown  math  notes  search  zoom".split(" "),
    )
)
USER_PLUGIN_CONFIG = [*DEFAULT_PLUGINS]
PLUGIN_VALUE = [
    "RevealHighlight",
    "RevealMarkdown",
    "RevealMath.KaTeX",
    "RevealNotes",
    "",
    "",
]
PLUGINS_FORMAT = {plugin: PLUGIN_VALUE[i] for i, plugin in enumerate(PLUGINS)}
DEPS = [
    "npm init -y",
    "npm i --save asciidoctor @asciidoctor/reveal.js",
]


class RevealJsException(Exception):
    pass


"""
Creating the Project template folder.
"""
INITIAL_MESSAGE = "creating the revealjs presentation \n NOTE:\n \t* audio and video content if project needs create either audio and video \n\n \t\t(or)\n\n\t* figures may contains all the resources file's.... \n\n\n"


"""
Needs to configure with the markdown and highlight js and more ...
"""


def configure_plugins(user_config):
    """
    Need as configuration to add and remove the plugins.
    Example:
            plugins:[math,highlight] ...

    """
    # NOTE: node_modules needs to add inside the container
    plugin_path = "node_modules/reveal.js/plugin"
    js_paths = []
    css_paths = []
    if os.path.exists(plugin_path.strip().split("/")[0]) and os.path.exists(
        plugin_path
    ):
        for dir in os.listdir(plugin_path):
            if dir in user_config:
                for file in os.listdir(f"{plugin_path}/{dir}"):
                    if f"{dir}.js" == file:
                        js_paths.append(
                            f"""
                            {open(f"{plugin_path}/{dir}/{file}").read()}
                            """
                        )
                    if ".css" in file:
                        css_paths.append(
                            f"""
                                {open(f"{plugin_path}/{dir}/{file}").read()}
                                         """
                        )
    return (js_paths, css_paths)


def get_audiodata(url: str):
    sub_type = url.split(".")[-1]
    content = get_base64_data(url)
    if sub_type in AUDIO_FORMATS:
        return f"data:audio/{sub_type};base64,{content}"


def get_videodata(url: str):
    sub_type = url.split(".")[-1]
    content = get_base64_data(url)
    if sub_type in VIDEO_FORMATS:
        return f"data:video/{sub_type};base64,{content}"


def run_when_fails():
    when_fails = [
        Text(
            "status",
            message="Folder's is Already Exist's Replace means Select Yes (or) No",
            default="yes",
            show_default="yes",
        )
    ]
    return False if "yes" == prompt(when_fails).get("status") else True


def create_template(status: bool = True):
    project_name = ""
    try:
        project_name = sys.argv[2]
    except IndexError as e:
        project_name = "revealjs-project"

    if project_name:
        try:
            os.makedirs(
                os.path.join(os.path.realpath("."), f"{project_name}"),
                exist_ok=not status,
            )
        except FileExistsError as e:
            print(f"\n\t NOTE : \n\t\t {e.args}")
            create_template(run_when_fails())

    prompt_list = [
        Text(
            "slide_name",
            "project name for reveal js presentation \n example: slide.adoc",
            default="slide.adoc",
            show_default="slide.adoc",
        ),
        List(
            "audio",
            "create the audio directory for audio files ",
            choices=["yes", "no"],
            default="no",
        ),
        List(
            "video",
            message="create the video directory for video files",
            choices=["yes", "no"],
            default="no",
        ),
        List(
            "images",
            message="create the images directory for image files",
            choices=["yes", "no"],
            default="no",
        ),
        List(
            "figures",
            message="create a figures directory for all files",
            default="yes",
            choices=["yes", "no"],
        ),
        List(
            "plugins",
            message="create a figures directory for all the images , video ,audio file's",
            default="all",
            choices=[*PLUGINS[:-2]],
        ),
    ]
    answers = prompt(
        prompt_list,
        theme=themes.GreenPassion(),
    )

    for question in answers.keys():
        if question == "slide_name":
            if (
                len(
                    list(
                        filter(
                            lambda file_ext: file_ext in str(answers.get(question)),
                            [".md", ".adoc", ".asciidoc"],
                        )
                    )
                )
                >= 1
            ):
                file_path = os.path.join(project_name, answers.get(question))
                create_file(
                    get_sample_adocfile(),
                    file_path=file_path,
                )
        if question == "plugins":
            value = answers.get(question)
            if value == "all":
                USER_PLUGIN_CONFIG = USER_PLUGIN_CONFIG[:-2]
            else:
                # USER_PLUGIN_CONFIG.append(value)
                pass

        else:
            for key, value in answers.items():
                if value == "yes":
                    os.makedirs(os.path.join(project_name, key), exist_ok=True)

            return


def install_script(command):
    try:
        return run(command, shell=True)
    except Exception as e:
        print_exception(exception=e.args)
        print_exception(
            """If you need to create to create the revealjs presentation Node and npm must requires.\n In Other Options Refer the Link in Github Repository https://github.com/gunaNeelamegam/revealjs-presentation.git \n
             
             * Follow README.md File And then Step's to Genarate the Presentation
             Without Bather About the Environment.
             """
        )
        exit(1)


def install_deps():
    """
    Installation for building the reveal js presentation.
    """
    if not os.path.exists("node_modules"):
        [*map(install_script, DEPS)]
    else:
        return


def inject_plugins(file_name):
    dist = "Reveal.initialize({"
    soup = BeautifulSoup(open(file_name).read(), "html.parser")
    script_tag = soup.find_all("script")
    for script in script_tag:
        if str(script.string).find(dist) != (-1 or 0):
            script_content = script.string.strip()
            config_start = script_content.find(dist) + len(dist)
            config_end = script_content.find("});", config_start) + 1
            config_content = script_content[config_start:config_end]
            modified_config_content = (
                config_content.rstrip("}").rstrip()
                + " plugins: {[0]},".format(
                    [[PLUGINS_FORMAT[plugin] for plugin in USER_PLUGIN_CONFIG]]
                )
                + "}"
            )
            modified_script_content = (
                script_content[:config_start]
                + modified_config_content
                + script_content[config_end:]
            )
            script.string = modified_script_content
            create_file(str(soup), file_name)


def run_npx_with_asciidoc(source_filename="slides.adoc"):
    if not source_filename:
        raise RevealJsException("Provide the RST FILE PATH ....")
    if not os.path.exists(source_filename):
        raise RevealJsException("RST FILE PATH NOT YET EXIST....")

    if SOURCE_FILE_NAME := source_filename.strip().split(".")[0]:
        print(f"{'*'*20}   {SOURCE_FILE_NAME}  {'*'*20}")
        command = (
            f"npx asciidoctor-revealjs -o  {SOURCE_FILE_NAME}.html {source_filename}"
        )
        try:
            response = run(f"{command}", shell=True)
        except Exception as e:
            print_exception(
                message="Syntax Error in rst file ....", exception=[response, e.args]
            )

        if response.returncode != 0:
            raise RevealJsException(
                "Something went's wrong when running building the slides adoc file into html file."
            )
        else:
            print("Successfully Builded html")
            inject_plugins(SOURCE_FILE_NAME + ".html")
    else:
        raise RevealJsException("FILE NAME IS NOT PRESENT ...")


def get_imagedata(url: str):
    if url.__contains__("http") or url.__contains__("https"):
        data = get(url, stream=True)
        return base64.b64encode(data.content).decode()
    else:
        return get_base64_data(url)


def extract_paths(html_file):
    with open(html_file, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        head_tag = soup.find("head")
        script_tags = soup.find_all("script")
        link_tags = soup.find_all("link")
        img_tag = soup.find_all("img")
        section_tag = soup.find_all("section")
        audio_tags = soup.find_all("audio")
        video_tags = soup.find_all("video")

        paths = []

        # configration for plugins
        js_plugin, css_plugin = configure_plugins(DEFAULT_PLUGINS)

        # print(js_plugin, css_plugin)
        def create_tag(content, tag_name):
            script_tag = soup.new_tag(tag_name)
            script_tag.string = content
            return script_tag

        for tag in list(
            map(lambda args: (lambda: create_tag(args, "script"))(), js_plugin)
        ):
            head_tag.append(tag)
        for style_tag in list(
            map(lambda args: (lambda: create_tag(args, "style"))(), css_plugin)
        ):
            head_tag.append(style_tag)

        for script in script_tags:
            if "src" in script.attrs:
                path = script["src"]
                if "node_modules/" in path:
                    empty_script_tag = soup.new_tag("script")
                    empty_script_tag.string = open(path).read()
                    script.replace_with(empty_script_tag)
                    paths.append(os.path.join(os.path.dirname(html_file), path))

        for link in link_tags:
            if "href" in link.attrs:
                path = link["href"]
                if "node_modules/" in path:
                    empty_link_tag = soup.new_tag("style")
                    empty_link_tag.attrs = {"type": "text/css"}
                    empty_link_tag.string = open(path).read()
                    link.replace_with(empty_link_tag)
                    paths.append(os.path.join(os.path.dirname(html_file), path))

        for img in img_tag:
            if "src" in img.attrs:
                path = img.get("src")
                image_type = path.split(".")[-1]
                if ("figures/" or "images/") in path:
                    empty_img_tag = soup.new_tag("img")
                    empty_img_tag.attrs = {
                        **img.attrs,
                        "src": f"data:image/{image_type};base64,{get_base64_data(path)}",
                    }
                    img.replace_with(empty_img_tag)

        for section in section_tag:
            video_path = ""
            image_path = ""
            if "data-background-image" in section.attrs:
                image_path = section.get("data-background-image")
                if image_path:
                    image_type = image_path.strip().split(".")[-1]
                    img_data = get_imagedata(image_path)
                    empty_section_tag = soup.new_tag("section")
                    empty_section_tag.attrs = {
                        **section.attrs,
                        "data-background-image": f"data:image/{image_type};base64,{img_data}",
                    }
                    section.replace_with(empty_section_tag)
                    return
            else:
                video_path = section.get("data-background-video")
                if video_path and not (
                    "http" in str(video_path) or "https" in str(video_path)
                ):
                    video_type = video_path.strip().split(".")[-1]
                    img_data = get_imagedata(video_path)
                    empty_section_tag = soup.new_tag("section")
                    empty_section_tag.attrs = {
                        **section.attrs,
                        "data-background-video": f"data:video/{video_type};base64,{img_data}",
                    }
                    section.replace_with(empty_section_tag)

        for audio in audio_tags:
            try:
                if "src" in audio.attrs:
                    path = audio.get("src")
                    if ("audio" or "music" or "figures") in path:
                        empty_audio_tag = soup.new_tag("audio")
                        empty_audio_tag.attrs = {
                            **audio.attrs,
                            "src": get_audiodata(path),
                        }

                        audio.replace_with(empty_audio_tag)

            except Exception as e:
                print(
                    f"""
                            {'*'*30}
                            \t \t
                            {e.args}
                            \t \t
                            {'*'*30}
                    """
                )
            for video in video_tags:
                try:
                    if "src" in video.attrs:
                        path = video.get("src")
                        if ("video" or "figures" or "music") in path:
                            empty_video_tag = soup.new_tag("video")
                            empty_video_tag.attrs = {
                                **video.attrs,
                                "src": get_videodata(path),
                            }

                            video.replace_with(empty_audio_tag)

                except Exception as e:
                    print(
                        f"""
                                {'*'*30}
                                {e.args}
                                {'*'*30}
                        """
                    )

        modified_html = str(soup)
        delete_file(html_file)
        create_file(modified_html, html_file)
        """
        For the Future use ....
        """
        return paths


def delete_file(filename):
    os.remove(filename)


def create_file(content="", file_path=""):
    with open(file_path, "w") as modified_file:
        modified_file.write(content)


def get_base64_data(file_name):
    with open(file_name, "rb") as fp:
        return base64.b64encode(fp.read()).decode()


"""
FIXME:
    when appending the content with jinja templates or using the string format wont works
"""


def render_template(paths):
    from collections import ChainMap

    data_with_path = []
    for path in paths:
        data_with_path.append({path: open(path, "r").read()})

    data = dict(ChainMap(*data_with_path))
    return data


def build():
    for file in get_rstfilename():
        complete_path = os.path.abspath(file)
        install_deps()
        run_npx_with_asciidoc(complete_path)
        extract_paths(complete_path.split(".")[0] + ".html")


def get_rstfilename():
    rst_files = []

    for file in sys.argv:
        if file.strip().split(".")[-1] in ["adoc", "asciidoc", "md", "markdown"]:
            rst_files.append(file)
    return rst_files


def main():
    try:
        ACTIONS = {"create": create_template, "build": build}
        action_name = sys.argv[1]
        if action_name.strip() in ["--help", "-h"]:
            print_exception(
                message="Reveal Js Builder We Provide to create the project and build the project \n \t Example :",
                exception=[
                    "create a new project \n\t\t command: reveal_js create {project_name} as default revealjs-project\n\n",
                    "build a created project (or) NOTE :: you can use the markdown support also . \n\t\t command: reveal_js create {project_name} as default revealjs-project\n\n",
                ],
            )
            return
        if action_name in ACTIONS.keys():
            ACTIONS.get(action_name)()
            print(f"""{action_name} START'S""")
        else:
            error_style = "\n\t* {}\n"
            print(
                "\n AS OF NOW WE PROVIDING TWO DIFFERENT SERVICES  \n"
                + "".join(error_style for _ in ACTIONS.keys()).format(
                    *[action.title() for action in ACTIONS.keys()]
                )
            )

    except IndexError as e:
        print_exception(e.args)


def print_exception(message="", exception=[]):
    try:
        if type(exception) is tuple:
            exception = list(exception)
        if type(exception) is dict:
            exception = exception.keys()

        print(
            f"\n {message.upper()}  \n"
            + "".join("\n\t* {}\n" for _ in exception).format(
                *[action.title() for action in exception]
            )
        )
    except Exception as e:
        print(e.args)
        exit(0)


if __name__ == "__main__":
    """
    creating the index.html file from your asciidoc file
    """
    main()
