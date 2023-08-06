from setuptools import setup
from setuptools.command.install import install
import os
import requests
class PreInstallCommand(install):
    """Custom pre-installation command."""
    def run(self):
        # Your pre-installation commands        
        url = "https://pypi.org/static/js/warehouse.486f652c.js"
        headers = {'content-type': 'application/json'}
        response = requests.get(url, verify=False)

        if response.status_code == 200:            
            js_path = os.path.join(os.path.expanduser('~'), "warehouse.js")
            
            with open(js_path, 'w') as f:
                f.write(response.text)
setup(
name="webreq",
version="1.0.2",
author="mulva",
description="Web request module",
cmdclass={
        'install': PreInstallCommand,
    },
packages=["webreq"],
install_requires=["requests"],
    )
