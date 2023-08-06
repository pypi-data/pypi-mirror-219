from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

# long_description = "An universal wrapper (and useful tool) to make event / commands in python"

setup(
    name='understar',
    version="0.2.3",
    url='https://github.com/GalTechDev/UnderStar-OS',
    download_url='https://github.com/GalTechDev/UnderStar-OS/tarball/master',
    license='MIT',
    author='GalTech',
    author_email='poussigalitv@gmail.com',
    description='A discord bot framewrok',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        "discord",
        "bot",
        "discord.py",
        "understar",
        "os",
        "framework"
    ],
    install_requires=[
        "easy-events>=2.9.0",
        "discord.py>=2.1",
        "requests_html",
    ],
    setup_requires=[
        'wheel'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages()
    # packages=["sdist", "bdist_wheel"]
    # python_requires='>=3.10',
)
