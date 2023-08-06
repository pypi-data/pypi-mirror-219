import setuptools
from pathlib import Path

setuptools.setup(
    name = 'jzx_env',
    version = '0.0.1',
    description = "A OpenAI Gym Env for jzx",
    long_description = Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(include="jzx_env*"),
    install_requires = ['gym']
)