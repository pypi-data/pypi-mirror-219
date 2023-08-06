from setuptools import setup

setup(
    name='Discus Synthetics',
    version='0.1.0b0',
    description='A package containing everything you need to finetune your LLMs',
    author='Discus Founders',
    author_email='founders@discus.ai',
    packages=['discus'],
    install_requires=['openai','pandas'],
)