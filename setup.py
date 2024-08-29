from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="ask",
    version="1.0",
    description="Ask something",
    py_modules=["ask"],
    entry_points={
        "console_scripts": [
            "ask=ask:main",
        ],
    },
    install_requires=required
)
