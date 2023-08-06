from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Extracts a part of the image specified by width and height from the given image file path using OpenCV.'''

# Setting up
setup(
    name="getpartofimg",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/getpartofimg',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'numpy', 'opencv_python'],
    keywords=['cv2', 'cut', 'opencv'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'numpy', 'opencv_python'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*