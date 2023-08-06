from setuptools import setup, find_packages

setup(
    name='qprom',
    version='0.1',
    url='https://github.com/MartinWie/qprom',
    author='Martin Wiechmann',
    author_email='donotsuspend@googlegroups.com',
    description='A Python-based CLI tool to quickly interact with OpenAIs GPT models instead of relying on the web interface.',
    packages=find_packages(),
    install_requires=['tiktoken', 'openai', 'argparse'],
)
