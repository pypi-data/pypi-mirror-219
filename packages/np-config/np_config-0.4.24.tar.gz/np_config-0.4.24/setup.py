# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_config']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1,<2',
 'backports.cached-property',
 'kazoo>=2.8,<2.9',
 'pyyaml>=5,<7',
 'requests>=2,<3',
 'singledispatch>=4.0.0,<5.0.0',
 'types-singledispatch>=4.0.0.1,<5.0.0.0',
 'typing-extensions>=4']

setup_kwargs = {
    'name': 'np-config',
    'version': '0.4.24',
    'description': 'Config fetching from file or Zookeeper - with local backup - repackaging code from AIBS mpeconfig.',
    'long_description': '# np_config\n\n\n### *For use on internal Allen Institute network*\n\n\n\nFetch configs from ZooKeeper nodes or .yaml/.json files:\n\n```python\nimport np_config\n\nzk_config: dict[str, str | int] = np_config.from_zk(\'/rigs/NP.1\')\n\nfile_config: dict[str, Any] = np_config.from_file(\'local_config.yaml\')\n\n```\n\n\nIf running on a machine attached to a Mindscope Neuropixels rig (`NP.0`, ..., `NP.3`), get rig-specific config info with:\n\n```python\nrig = np_config.Rig()\n\nname: str = rig.id                            # "NP.1"\nindex: int = rig.idx                          # 1\n\nacquisition_pc_hostname: str = rig.acq        # "W10DT713843"\nconfig: dict[str, str | int] = rig.config     # specific to NP.1\npaths: dict[str, pathlib.Path] = rig.paths    # using values from rig.config\n```\n\n\n\nIf not running on a rig-attached machine, get the config for a particular rig by supplying rig-index as an `int` to `Rig`:\n\n```python\nnp1 = np_config.Rig(1)\n\nnp1_mvr_data_root: pathlib.Path = np.paths[\'MVR\']\n```\n\n\n***\n\n\n- the Mindscope ZooKeeper server is at `eng-mindscope:2181`\n- configs can be added via ZooNavigator webview:\n  [http://eng-mindscope:8081](http://eng-mindscope:8081)\n- or more conveniently, via an extension for VSCode such as [gaoliang.visual-zookeeper](https://marketplace.visualstudio.com/items?itemName=gaoliang.visual-zookeeper)\n',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben Hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
