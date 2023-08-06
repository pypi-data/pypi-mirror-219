from setuptools import setup, find_packages
import codecs
import os

VERSION                     = "0.0.3"
DESCRIPTION                 = "Browser based fully customisable User Interface"
LONG_DESCRIPTION            = "pyriddle gives you a simple and powerfull way to display graphics, text infos, video stream and so on, only using your browser as support."
if os.path.isfile("./README.md"):
    with open("./README.md", 'r') as f:
        LONG_DESCRIPTION    = f.read()

# Setting up
setup(
    name="pyriddle",
    version=VERSION,
    author="Tech0ne",
    author_email="<null@noemail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["flask", "simple-websocket", "flask_socketio", "opencv-python"],
    keywords=["python", "ui", "stream", "video", "stats"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
