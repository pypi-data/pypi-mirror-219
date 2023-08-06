import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tellosync',
    version='0.1.0',
    author='Ezra Fielding, Vincent Wu',
    author_email='ezra.fielding@gmail.com, vwu1888@gmail.com',
    description='An easy framework to support DJI Tello scripting in Python 3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vwu1888/easyTello',
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python',
        'pyserial'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
