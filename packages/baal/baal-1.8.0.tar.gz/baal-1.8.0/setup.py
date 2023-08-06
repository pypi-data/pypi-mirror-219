# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baal',
 'baal.active',
 'baal.active.dataset',
 'baal.active.heuristics',
 'baal.bayesian',
 'baal.calibration',
 'baal.metrics',
 'baal.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=6.2.0',
 'h5py>=3.4.0,<4.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'structlog>=21.1.0,<22.0.0',
 'torch>=1.6.0',
 'torchmetrics>=0.9.3,<0.10.0',
 'tqdm>=4.62.2,<5.0.0']

extras_require = \
{'nlp': ['transformers>=4.10.2', 'datasets>=1.11.0'],
 'vision': ['torchvision>=0.7.0', 'lightning-flash>=0.7.5']}

setup_kwargs = {
    'name': 'baal',
    'version': '1.8.0',
    'description': 'Library to enable Bayesian active learning in your research or labeling work.',
    'long_description': '<p align="center">\n  <img height=15% width=25% src="https://i.imgur.com/Zdzb2QZ.png" style="max-width: 100%;border-radius: 25%;">\n  <h1 align="center">Bayesian Active Learning (Baal)\n   <br>\n  <a href="https://github.com/baal-org/baal/actions/workflows/pythonci.yml">\n    <img alt="Python CI" src="https://github.com/baal-org/baal/actions/workflows/pythonci.yml/badge.svg"/>\n  </a>\n  <a href="https://baal.readthedocs.io/en/latest/?badge=latest">\n    <img alt="Documentation Status" src="https://readthedocs.org/projects/baal/badge/?version=latest"/>\n  </a>\n  <a href="https://join.slack.com/t/baal-world/shared_invite/zt-z0izhn4y-Jt6Zu5dZaV2rsAS9sdISfg">\n    <img alt="Slack" src="https://img.shields.io/badge/slack-chat-green.svg?logo=slack"/>\n  </a>\n  <a href="https://github.com/Elementai/baal/blob/master/LICENSE">\n    <img alt="Licence" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/>\n  </a>\n  <a href="https://calendly.com/baal-org/30min">\n    <img alt="Office hours" src="https://img.shields.io/badge/Office hours-Calendly-blue.svg"/>\n  </a>\n  <a href="https://pepy.tech/project/baal">\n    <img alt="Downloads" src="https://pepy.tech/badge/baal"/>\n  </a>\n\n  </h1>\n</p>\n\nBaal is an active learning library that supports both industrial applications and research usecases.\n\nRead the documentation at https://baal.readthedocs.io.\n\nOur paper can be read on [arXiv](https://arxiv.org/abs/2006.09916). It includes tips and tricks to make active learning\nusable in production.\n\nFor a quick introduction to Baal and Bayesian active learning, please see these links:\n\n- [Seminar with Label Studio](https://www.youtube.com/watch?v=HG7imRQN3-k)\n- [User guide](https://baal.readthedocs.io/en/latest/user_guide/index.html)\n- [Bayesian active learning presentation](https://drive.google.com/file/d/13UUDsS1rvqDnXza7L0j4bnqyhOT5TDSt/view?usp=sharing)\n\n*Baal was initially developed at [ElementAI](https://www.elementai.com/) (acquired by ServiceNow in 2021), but is now independant.*\n\n\n## Installation and requirements\n\nBaal requires `Python>=3.8`.\n\nTo install Baal using pip: `pip install baal`\n\nWe use [Poetry](https://python-poetry.org/) as our package manager.\nTo install Baal from source: `poetry install`\n\n## Papers using Baal\n\n- [Bayesian active learning for production, a systematic study and a reusable library\n  ](https://arxiv.org/abs/2006.09916) (Atighehchian et al. 2020)\n- [Synbols: Probing Learning Algorithms with Synthetic Datasets\n  ](https://nips.cc/virtual/2020/public/poster_0169cf885f882efd795951253db5cdfb.html) (Lacoste et al. 2020)\n- [Can Active Learning Preemptively Mitigate Fairness Issues?\n  ](https://arxiv.org/pdf/2104.06879.pdf) (Branchaud-Charron et al. 2021)\n- [Active learning with MaskAL reduces annotation effort for training Mask R-CNN](https://arxiv.org/abs/2112.06586) (\n  Blok et al. 2021)\n- [Stochastic Batch Acquisition for Deep Active Learning](https://arxiv.org/abs/2106.12059) (Kirsch et al. 2022)\n\n# What is active learning?\n\nActive learning is a special case of machine learning in which a learning algorithm is able to interactively query the\nuser (or some other information source) to obtain the desired outputs at new data points\n(to understand the concept in more depth, refer to our [tutorial](https://baal.readthedocs.io/en/latest/)).\n\n## Baal Framework\n\nAt the moment Baal supports the following methods to perform active learning.\n\n- Monte-Carlo Dropout (Gal et al. 2015)\n- MCDropConnect (Mobiny et al. 2019)\n- Deep ensembles\n- Semi-supervised learning\n\nIf you want to propose new methods, please submit an issue.\n\nThe **Monte-Carlo Dropout** method is a known approximation for Bayesian neural networks. In this method, the Dropout\nlayer is used both in training and test time. By running the model multiple times whilst randomly dropping weights, we\ncalculate the uncertainty of the prediction using one of the uncertainty measurements\nin [heuristics.py](baal/active/heuristics/heuristics.py).\n\nThe framework consists of four main parts, as demonstrated in the flowchart below:\n\n- ActiveLearningDataset\n- Heuristics\n- ModelWrapper\n- ActiveLearningLoop\n\n<p align="center">\n  <img src="docs/research/literature/images/Baalscheme.svg">\n</p>\n\nTo get started, wrap your dataset in our _[**ActiveLearningDataset**](baal/active/dataset.py)_ class. This will ensure\nthat the dataset is split into\n`training` and `pool` sets. The `pool` set represents the portion of the training set which is yet to be labelled.\n\nWe provide a lightweight object _[**ModelWrapper**](baal/modelwrapper.py)_ similar to `keras.Model` to make it easier to\ntrain and test the model. If your model is not ready for active learning, we provide Modules to prepare them.\n\nFor example, the _[**MCDropoutModule**](baal/bayesian/dropout.py)_ wrapper changes the existing dropout layer to be used\nin both training and inference time and the `ModelWrapper` makes the specifies the number of iterations to run at\ntraining and inference.\n\nFinally, _[**ActiveLearningLoop**](baal/active/active_loop.py)_ automatically computes the uncertainty and label the most\nuncertain items in the pool.\n\nIn conclusion, your script should be similar to this:\n\n```python\ndataset = ActiveLearningDataset(your_dataset)\ndataset.label_randomly(INITIAL_POOL)  # label some data\nmodel = MCDropoutModule(your_model)\nmodel = ModelWrapper(model, your_criterion)\nactive_loop = ActiveLearningLoop(dataset,\n                                 get_probabilities=model.predict_on_dataset,\n                                 heuristic=heuristics.BALD(),\n                                 iterations=20, # Number of MC sampling.\n                                 query_size=QUERY_SIZE)  # Number of item to label.\nfor al_step in range(N_ALSTEP):\n    model.train_on_dataset(dataset, optimizer, BATCH_SIZE, use_cuda=use_cuda)\n    metrics = model.test_on_dataset(test_dataset, BATCH_SIZE)\n    # Label the next most uncertain items.\n    if not active_loop.step():\n        # We\'re done!\n        break\n```\n\nFor a complete experiment, see _[experiments/vgg_mcdropout_cifar10.py](experiments/vgg_mcdropout_cifar10.py)_ .\n\n### Re-run our Experiments\n\n```bash\ndocker build [--target base_baal] -t baal .\ndocker run --rm baal --gpus all python3 experiments/vgg_mcdropout_cifar10.py\n```\n\n### Use Baal for YOUR Experiments\n\nSimply clone the repo, and create your own experiment script similar to the example\nat _[experiments/vgg_mcdropout_cifar10.py](experiments/vgg_mcdropout_cifar10.py)_. Make sure to use the four main parts of Baal\nframework. _Happy running experiments_\n\n### Contributing!\n\nTo contribute, see [CONTRIBUTING.md](./CONTRIBUTING.md).\n\n### Who We Are!\n\n"There is passion, yet peace; serenity, yet emotion; chaos, yet order."\n\nThe Baal team tests and implements the most recent papers on uncertainty estimation and active learning.\n\nCurrent maintainers:\n\n- [Parmida Atighehchian](mailto:patighehchian@twitter.com)\n- [Frédéric Branchaud-Charron](mailto:frederic.branchaud-charron@gmail.com)\n- [George Pearse](georgehwp26@gmail.com)\n\n### How to cite\n\nIf you used Baal in one of your project, we would greatly appreciate if you cite this library using this Bibtex:\n\n```\n@misc{atighehchian2019baal,\n  title={Baal, a bayesian active learning library},\n  author={Atighehchian, Parmida and Branchaud-Charron, Frederic and Freyberg, Jan and Pardinas, Rafael and Schell, Lorne\n          and Pearse, George},\n  year={2022},\n  howpublished={\\url{https://github.com/baal-org/baal/}},\n}\n```\n\n### Licence\n\nTo get information on licence of this API please read [LICENCE](./LICENSE)\n',
    'author': 'Parmida Atighehchian',
    'author_email': 'parmida.atighehchian@servicenow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ElementAI/baal/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
