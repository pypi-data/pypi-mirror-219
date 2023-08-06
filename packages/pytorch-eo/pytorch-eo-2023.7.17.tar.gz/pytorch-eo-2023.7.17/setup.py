# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_eo',
 'pytorch_eo.config',
 'pytorch_eo.datasets',
 'pytorch_eo.datasets.big_earth_net',
 'pytorch_eo.datasets.eurosat',
 'pytorch_eo.datasets.land_cover_net',
 'pytorch_eo.datasets.sen12ms',
 'pytorch_eo.datasets.sensors',
 'pytorch_eo.datasets.ucmerced',
 'pytorch_eo.metrics',
 'pytorch_eo.tasks',
 'pytorch_eo.tasks.classification',
 'pytorch_eo.tasks.segmentation',
 'pytorch_eo.utils',
 'pytorch_eo.utils.datasets']

package_data = \
{'': ['*']}

install_requires = \
['lightning>=2.0.1,<3.0.0',
 'pandas>=1.5.3,<2.0.0',
 'rasterio>=1.3.5.post1,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'torch>=2.0.1,<3.0.0',
 'torchmetrics>=1.0.1,<2.0.0',
 'torchvision>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'pytorch-eo',
    'version': '2023.7.17',
    'description': 'Deep Learning for Earth Observation',
    'long_description': '# Pytorch EO\n\nDeep Learning for Earth Observation applications and research.\n\n> 🚧 This project is in early development, so bugs and breaking changes are expected until we reach a stable version.\n\n## Installation\n\n```\npip install pytorch-eo\n```\n\n## Examples\n\nLearn by doing with our [examples](https://github.com/earthpulse/pytorch_eo/tree/main/examples).\n\n### Ready to use Datasets\n\n- [EuroSAT](https://github.com/phelber/EuroSAT).\n- [UCMerced](http://weegee.vision.ucmerced.edu/datasets/landuse.html) Land Use Dataset.\n- [BigEarthNet](https://mlhub.earth/data/bigearthnet_v1).\n<!-- - [LandCoverNet](https://mlhub.earth/10.34911/rdnt.d2ce8i) -->\n\n### Tutorials\n\nLearn how to build with Pytorch EO with our [tutorials](https://github.com/earthpulse/pytorch_eo/tree/main/tutorials).\n\n## Challenges\n\nPytorchEO has been used in the following challenges:\n\n- [EUROAVIA](./challenges/euroavia_hackathon_21) Mission: European Students Space Hackathon, 2021.\n- [On Cloud N](./challenges/OnCloudN): Cloud Cover Detection Challenge (DrivenData, 2021).\n\n<!-- ### Build your own Datasets\n\nUsing SCAN you can annotate your own data and access it directly through Pytorch EO. -->\n\n<!-- ## Research\n\nPytorch EO can be a useful tool for research:\n\n- Flexibility: build and experiment with new models for EO applications.\n- Reproducibility: use same data splits and random seeds to compare with others.\n\nSee the [examples](https://github.com/earthpulse/pytorch_eo/tree/main/examples).\n\n## Production\n\nPytorch EO was built with production in mind from the beginning:\n\n- Optimize model for production.\n- Export models to torchscript.\n- Upload models to our Models Universe\n- Use models directly through SPAI\n\nSee the [examples](https://github.com/earthpulse/pytorch_eo/tree/main/examples). -->\n\n<!-- ## Documentation\n\nRead our [docs](https://earthpulse.github.io/pytorch_eo/). -->\n\n## Contributing\n\nRead the [CONTRIBUTING](https://github.com/earthpulse/pytorch_eo/blob/main/CONTRIBUTING.md) guide.\n',
    'author': 'EarthPulse',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
