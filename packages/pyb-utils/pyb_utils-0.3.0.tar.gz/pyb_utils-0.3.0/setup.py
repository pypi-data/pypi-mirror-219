# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyb_utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'pybullet>=3.2.1,<4.0.0',
 'spatialmath-python>=1.0.0']

setup_kwargs = {
    'name': 'pyb-utils',
    'version': '0.3.0',
    'description': 'Basic utilities for PyBullet, including collision detection, ghost (i.e. visual-only) objects, and cameras.',
    'long_description': "# pyb_utils: utilities for PyBullet\n\nThis is a collection of utilities I've found useful for working with PyBullet,\nincluding:\n* Collision detection: conveniently set up shortest distance computations and\n  collision checking between arbitrary objects in arbitrary configurations with\n  PyBullet. See the accompanying [blog post](https://adamheins.com/blog/collision-detection-pybullet).\n* Ghost objects: add purely visual objects to the simulation, optionally\n  attached to another body.\n* Camera: virtual camera from which to get RGBA, depth, segmentation, and point\n  cloud data. Also provides video recording using OpenCV.\n* Convenience class for easily creating rigid bodies.\n* Versions of some PyBullet functions that return *named* tuples, for easy\n  field access.\n* Basic quaternion functions.\n\n## Install and run\nThis package requires **Python 3.7+**. It has been tested on Ubuntu 16.04,\n18.04, and 20.04.\n\n### From pip\n```\npip install pyb_utils\n```\n\n### From source\nClone the repo:\n```bash\ngit clone https://github.com/adamheins/pyb_utils\ncd pyb_utils\n```\n\nInstall using [poetry](https://python-poetry.org/):\n```bash\npoetry install\npoetry run python examples/collision_detection_example.py  # for example\n```\n\nOr using pip:\n```bash\npython -m pip install .\n```\n\n## Usage and examples\nThis package provides a few basic quality of life utilities. First, PyBullet\nrepresents rotations using quaternions (in `[x, y, z, w]` order). We provide a\nfew helper routines to convert to rotation matrices and rotate points (using\n[spatialmath](https://github.com/bdaiinstitute/spatialmath-python) under the\nhood):\n```python\n>>> import pyb_utils\n>>> q = (0, 0, np.sqrt(2) / 2, np.sqrt(2) / 2)  # 90 deg rotation about z-axis\n\n>>> pyb_utils.quaternion_to_matrix(q)  # convert to rotation matrix\narray([[ 1.,  0.,  0.],\n       [ 0., -0., -1.],\n       [ 0.,  1., -0.]])\n\n>>> pyb_utils.quaternion_multiply(q, q)  # rotate two quaternions together\narray([0, 0, -1, 0])                     # 180 deg rotate about z\n\n>>> pyb_utils.quaternion_rotate(q, [1, 0, 0])  # rotate a point\narray([0, 1, 0])\n```\n\nSecond, we provide a simple class to quickly create rigid bodies\nprogrammatically, which is useful for adding basic objects to manipulate or act\nas obstacles:\n```python\n>>> import pybullet as pyb\n>>> import pyb_utils\n\n>>> pyb.connect(pyb.GUI)\n\n# create a 1x1x1 cube at the origin\n>>> box = pyb_utils.BulletBody.box(position=[0, 0, 0], half_extents=[0.5, 0.5, 0.5])\n\n# put a ball on top\n>>> ball = pyb_utils.BulletBody.sphere(position=[0, 0, 1.5], radius=0.5)\n\n# now put it somewhere else\nball.set_pose(position=[2, 0, 0.5])\n```\n\nThird, we wrap some PyBullet functions to return *named* tuples, rather than\nnormal tuples. When the tuples have 10+ fields in them, it is rather helpful to\nhave names! The names and parameters of these functions are exactly the same as\nthe underlying PyBullet ones, to make swapping effortless. Continuing our\nprevious example:\n```python\n# built-in PyBullet method\n# the output is not easy to read!\n>>> pyb.getDynamicsInfo(box.uid, -1)\n(1.0,\n 0.5,\n (0.16666666666666666, 0.16666666666666666, 0.16666666666666666),\n (0.0, 0.0, 0.0),\n (0.0, 0.0, 0.0, 1.0),\n 0.0,\n 0.0,\n 0.0,\n -1.0,\n -1.0,\n 2,\n 0.001)\n\n# switch to the pyb_utils version\n# now we can access fields by name\n>>> info = pyb_utils.getDynamicsInfo(box.uid, -1)\n>>> info.mass\n1.0\n>>> info.localInertiaPos\n(0.0, 0.0, 0.0)\n```\n\nAnd there's more! You can find example scripts of all of this package's\nutilities in the `examples/` directory:\n\n* [rigid bodies](examples/bodies_example.py)\n* [camera](examples/camera_example.py)\n* [collision detection](examples/collision_detection_example.py)\n* [ghost objects](examples/ghost_object_example.py)\n* [named tuples](examples/named_tuples_example.py)\n* [video](examples/video_example.py)\n\n## Known issues\nFeel free to open issues (or better yet, a pull request!) if you find a\nproblem. Currently known issues:\n\n* Video recording does not output MP4 videos correctly. The AVI format works,\n  however.\n* Ghost objects sometimes flicker (spooky, but undesirable).\n\n## License\n[MIT](https://github.com/adamheins/pyb_utils/blob/main/LICENSE)\n",
    'author': 'Adam Heins',
    'author_email': 'mail@adamheins.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
