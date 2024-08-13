from setuptools import setup, find_packages

def read_requirements():
  with open("requirements.txt") as req:
    return req.read().splitlines()

setup(
    name="to_do_cli_app",
    version="0.1.0",
    packages=find_packages(include=['to_do_cli_app', 'to_do_cli_app.*']),
    include_package_data=True,
    package_data={
      'to_do_cli_app': [
            'config.json',  # Include config.json in the package
            'tasks/*',      # Include all files in the tasks directory
        ],
    },
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "todo-cli=to_do_cli_app.main:main",
        ],
    },
    author="luxiopppp",
    description="A little task manager inside the terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/luxiopppp/to-do-cli-app',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.12.3',
)

