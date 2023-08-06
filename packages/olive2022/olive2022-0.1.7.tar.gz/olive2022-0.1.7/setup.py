# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['olive2022']
install_requires = \
['pyyaml>=6.0,<7.0',
 'sinfonia-tier3>=0.7.0,<0.8.0',
 'tqdm>=4.64.1,<5.0.0',
 'xdg>=5.1.1,<6.0.0',
 'yarl>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['olive2022 = olive2022:main']}

setup_kwargs = {
    'name': 'olive2022',
    'version': '0.1.7',
    'description': 'Edge-native virtual desktop application',
    'long_description': "# Olive 2022\n\nEdge-native virtual desktop application that uses the\n[Sinfonia](https://github.com/cmusatyalab/sinfonia) framework to discover a\nnearby cloudlet to run the virtual machine.\n\nVirtual machine images from [Olivearchive](https://olivearchive.org) are\nconverted from their original vmnetx package format to a containerDisk\nthat can be executed with KubeVirt. The containerDisk images can be pushed into\na private Docker registry.\n\n\n## Installation\n\nOlive2022 depends on an available VNC client. I've found that virt-viewer from\nlibvirt generally does a good job. On a Debian/Ubuntu system this can be\ninstalled with.\n\n```\nsudo apt install virt-viewer\n```\n\nIt is best to manage the installation of olive2022 in a separate virtualenv with\n[pipx](https://pypa.github.io/pipx/installation/).\n\n```\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\nOnce these dependencies are in place, installation should be fairly\nstraightforward, even specifying a python version should only be necessary if\nthe system default happens to be older than Python-3.7.\n\n```\npipx install olive2022\n```\n\nIf installation fails at any point, there are various troubleshooting tips at\nthe end of this document.\n\n\n## Usage\n\n`olive2022 install` creates a .desktop file to declare a handler for\nvmnetx+https URLs.\n\nWhen you then 'Launch' a virtual machine from the Olivearchive website, the\nhandler will execute `olive2022 launch` with the VMNetX URL for the virtual\nmachine image.\n\n\n## Internals\n\n`olive2022 launch` hashes the VMNetX URL to a Sinfonia UUID, and uses\n`sinfonia-tier3` to request the relevant backend to be started on a nearby\ncloudlet. When deployment has started, `sinfonia-tier3` will create a local\nwireguard tunnel endpoint and runs `olive2022 stage2` which waits for the\ndeployment to complete by probing if the VNC endpoint has become accessible.\nIt will then try to run remote-viewer (from the virt-viewer package),\ngvncviewer, or vncviewer.\n\n\n## Converting VMNetX packages\n\n`olive2022 convert` will take a VMNetX URL, download the vmnetx format package\nfile and convert it to a containerDisk image and associated Sinfonia recipe.\nThe Docker registry to push the containerDisk image to can be set with the\n`OLIVE2022_REGISTRY` environment variable. If it is a private repository, the\nnecessary pull credentials to add to the recipe can be specified with\n`OLIVE2022_CREDENTIALS=<username>:<access_token>`.\n\n\n## Installation troubleshooting\n\n#### `/usr/bin/python3: No module named pip`\n\nPip is not installed on your system. On Debian/Ubuntu systems, to reduce the\nchance of interfering with packaged Python modules, the default Python\ninstallation does not install pip and even disables the `python3 -m ensurepip`\nway of installing a recent version of the pip package manager. You have to\ninstall the python3-pip and python3-venv packages.\n\n```\nsudo apt install python3-pip python3-venv\n```\n\n#### `pipx: command not found`\n\n`python3 -m pipx ensurepath` is only able to fix the PATH environment for\nsome (mostly bourne-like) shells. If you are using bash/sh/fish/zsh it may be\nsufficient to restart your terminal to pick up the new path.\n\nWith csh/tcsh you will probably have to add the following to your `.login` or\n`.cshrc` files and/or run `rehash` to pick up any new binaries.\n\n```\nset path = ( $path $HOME/.local/bin )\n```\n\n#### `ERROR: Could not find a version that satisfies the requirement olive2022 (from versions: none)`\n\nBecause Olive2022 depends on Python-3.7 or newer, installation fails with this\nerror when the default Python interpreter is older. On Ubuntu 18.04 you can\ninstall a newer Python interpreter and explicitly specify it as an alternate\ninterpreter version when installing with pipx.\n\n```\nsudo apt install python3.8\npipx install --python python3.8 olive2022\n```\n",
    'author': 'Carnegie Mellon University',
    'author_email': 'satya+group@cs.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cmusatyalab/olive2022',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
