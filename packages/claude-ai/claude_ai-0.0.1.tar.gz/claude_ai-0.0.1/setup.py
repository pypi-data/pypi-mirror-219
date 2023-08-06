from setuptools import setup, find_packages


setup(
    name='claude_ai',
    version='0.0.1',
    url='https://github.com/boyueluzhipeng/claude_ai',
    py_modules=find_packages(),

    install_requires=[
        'requests',
    ],
)
