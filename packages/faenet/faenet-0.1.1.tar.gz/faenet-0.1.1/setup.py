# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faenet']

package_data = \
{'': ['*']}

install_requires = \
['e3nn>=0.5.1', 'mendeleev>=0.12,<0.13', 'torch>=1.12']

setup_kwargs = {
    'name': 'faenet',
    'version': '0.1.1',
    'description': "PyTorch implementation for FAENet from 'FAENet: Frame Averaging Equivariant GNN for Materials Modeling'",
    'long_description': '<p align="center">\n<strong><a href="https://github.com/vict0rsch/faenet" target="_blank">💻&nbsp;&nbsp;Code</a></strong>\n<strong>&nbsp;&nbsp;•&nbsp;&nbsp;</strong>\n<strong><a href="https://faenet.readthedocs.io/" target="_blank">Docs&nbsp;&nbsp;📑</a></strong>\n</p>\n\n<p align="center">\n    <a>\n\t    <img src=\'https://img.shields.io/badge/python-3.8%2B-blue\' alt=\'Python\' />\n\t</a>\n\t<a href=\'https://faenet.readthedocs.io/en/latest/?badge=latest\'>\n    \t<img src=\'https://readthedocs.org/projects/faenet/badge/?version=latest\' alt=\'Documentation Status\' />\n\t</a>\n    <a href="https://github.com/psf/black">\n\t    <img src=\'https://img.shields.io/badge/code%20style-black-black\' />\n\t</a>\n<a href="https://pytorch.org">\n<img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white"/>\n</a>\n</p>\n<br/>\n\n# FAENet: Frame Averaging Equivariant GNN for Materials modeling\n\n\nThis repository contains an implementation of the paper *FAENet: Frame Averaging Equivariant GNN for Materials modeling*, accepted at ICML 2023. More precisely, you will find:\n\n* `FrameAveraging`: the transform that projects your pytorch-geometric data into the canonical space defined in the paper.\n* `FAENet` GNN model for material modeling. \n* `model_forward`: a high-level forward function that computes appropriate model predictions for the Frame Averaging method, i.e. handling the different frames and mapping to equivariant predictions. \n\nAlso: https://github.com/vict0rsch/faenet\n\n## Installation\n\n```\npip install faenet\n```\n\n⚠️ The above installation requires `Python >= 3.8`, [`torch > 1.11`](https://pytorch.org/get-started/locally/), [`torch_geometric > 2.1`](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html#) to the best of our knowledge. Both `mendeleev` and `pandas` package are also required to derive physics-aware atom embeddings in FAENet.\n\n## Getting started\n\n### Frame Averaging Transform\n\n`FrameAveraging` is a Transform method applicable to pytorch-geometric `Data` object. You can choose among several options ranging from *Full FA* to *Stochastic FA* (in 2D or 3D) including data augmentation *DA*. This method shall be applied in the `get_item()` function of your `Dataset` class. Note that although this transform is specific to pytorch-geometric data objects, it can be easily extended to new settings since the core functions `frame_averaging_2D()` and `frame_averaging_3D()` generalise to other data format. \n\n```python\nimport torch\nfrom faenet.transform import FrameAveraging\n\nframe_averaging = "3D"  # symmetry preservation method used: {"3D", "2D", "DA", ""}:\nfa_method = "stochastic"  # the frame averaging method: {"det", "all", "se3-stochastic", "se3-det", "se3-all", ""}:\ntransform = FrameAveraging(frame_averaging, fa_method)\ntransform(g)  # transform the PyG graph g \n```\n\n### Model forward for Frame Averaging\n\n`model_forward()` aggregates model predictions when Frame Averaging is applied, as stipulated by the Equation (1) of the paper. It must be applied. \n\n```python\nfrom faenet.fa_forward import model_forward\n\npreds = model_forward(\n    batch=batch,   # batch from, dataloader\n    model=model,  # FAENet(**kwargs)\n    frame_averaging="3D", # ["2D", "3D", "DA", ""]\n    mode="train",  # for training \n    crystal_task=True,  # for crystals, with pbc conditions\n)\n```\n\n### FAENet GNN \n\nImplementation of the FAENet GNN model, compatible with any dataset or transform. In short, FAENet is a very simple, scalable and expressive model. Since does not explicitly preserve data symmetries, it has the ability to process directly and unrestrictedly atom relative positions, which is very efficient. Note that the training procedure is not given here. \n\n```python\nfrom faenet.model import FAENet\n\npreds = FAENet(**kwargs)\nmodel(batch)\n```\n\n![FAENet architecture](examples/data/faenet-archi.png)\n\n### Eval \n\nThe `eval_model_symmetries()` function helps you evaluate the equivariant, invariant and other properties of a model, as we did in the paper. \n\n### Tests\n\nThe `/tests` folder contains several useful unit-tests. Feel free to have a look at them to explore how the model can be used. For more advanced examples, please refer to the full [repository](https://github.com/RolnickLab/ocp) used in our ICML paper to make predictions on OC20 IS2RE, S2EF, QM9 and QM7-X dataset. \n\nThis requires [`poetry`](https://python-poetry.org/docs/). Make sure to have `torch` and `torch_geometric` installed in your environment before you can run the tests. Unfortunately because of CUDA/torch compatibilities, neither `torch` nor `torch_geometric` are part of the explicit dependencies and must be installed independently.\n\n```bash\ngit clone git@github.com:vict0rsch/faenet.git\npoetry install --with dev\npytest --cov=faenet --cov-report term-missing\n```\n\nTesting on Macs you may encounter a [Library Not Loaded Error](https://github.com/pyg-team/pytorch_geometric/issues/6530)\n\n### Contact\n\nAuthors: Alexandre Duval (alexandre.duval@mila.quebec) and Victor Schmidt (schmidtv@mila.quebec). We welcome your questions and feedback via email or GitHub Issues.\n\n',
    'author': 'Victor Schmidt',
    'author_email': 'vsch@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
