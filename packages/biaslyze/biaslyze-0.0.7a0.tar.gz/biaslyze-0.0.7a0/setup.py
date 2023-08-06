# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biaslyze', 'biaslyze.bias_detectors', 'biaslyze.results']

package_data = \
{'': ['*']}

install_requires = \
['bertopic==0.13.0',
 'bokeh>=3.1.0,<4.0.0',
 'dash>=2.11.1,<3.0.0',
 'eli5>=0.13.0,<0.14.0',
 'jupyterlab>=3.5.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy==1.23.2',
 'nvidia-cublas-cu11>=11.11.3.6,<12.0.0.0',
 'nvidia-cuda-cupti-cu11>=11.8.87,<12.0.0',
 'nvidia-cuda-nvrtc-cu11>=11.8.89,<12.0.0',
 'nvidia-cuda-runtime-cu11>=11.8.89,<12.0.0',
 'nvidia-cudnn-cu11>=8.9.1.23,<9.0.0.0',
 'nvidia-cufft-cu11>=10.9.0.58,<11.0.0.0',
 'nvidia-curand-cu11>=10.3.0.86,<11.0.0.0',
 'nvidia-cusolver-cu11>=11.4.1.48,<12.0.0.0',
 'nvidia-cusparse-cu11>=11.7.5.86,<12.0.0.0',
 'nvidia-nccl-cu11>=2.16.5,<3.0.0',
 'nvidia-nvtx-cu11>=11.8.86,<12.0.0',
 'pandas>=1.5.3,<2.0.0',
 'plotly>=5.15.0,<6.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy==1.8.0',
 'spacy>=3.5.0,<4.0.0',
 'transformers>=4.26.1,<5.0.0',
 'triton>=2.0.0.post1,<3.0.0',
 'umap-learn>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'biaslyze',
    'version': '0.0.7a0',
    'description': 'The NLP Bias Identification Toolkit',
    'long_description': '\n<div align="center">\n  <img src="resources/biaslyze-logo-no-bg.png" alt="Biaslyze" height="220px">\n  <h1>The NLP Bias Identification Toolkit</h1>\n</div>\n\n<div align="center">\n    <a href="https://github.com/biaslyze-dev/biaslyze/blob/main/LICENSE">\n        <img alt="licence" src="https://img.shields.io/github/license/biaslyze-dev/biaslyze">\n    </a>\n    <a href="https://pypi.org/project/biaslyze/">\n        <img alt="pypi" src="https://img.shields.io/pypi/v/biaslyze">\n    </a>\n    <a href="https://pypi.org/project/biaslyze/">\n        <img alt="pypi" src="https://img.shields.io/pypi/pyversions/biaslyze">\n    </a>\n</div>\n\n\nBias is often subtle and difficult to detect in NLP models, as the protected attributes are less obvious and can take many forms in language (e.g. proxies, double meanings, ambiguities etc.). Therefore, technical bias testing is a key step in avoiding algorithmically mediated discrimination. However, it is currently conducted too rarely due to the effort involved, missing resources or lack of awareness for the problem.\n\nBiaslyze helps to get started with the analysis of bias within NLP models and offers a concrete entry point for further impact assessments and mitigation measures. Especially for developers, researchers and teams with limited resources, our toolbox offers a low-effort approach to bias testing in NLP use cases.\n\n## Supported Models\n\nAll text classification models with probability output are supported. This includes models from scikit-learn, tensorflow, pytorch, huggingface transformers and others. \nSee the tutorials section for examples.\n\n## Installation\n\nInstallation can be done using pypi:\n```bash\npip install biaslyze\n```\n\nThen you need to download the required spacy models:\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Quickstart\n\n```python\nfrom biaslyze.bias_detectors import CounterfactualBiasDetector\n\nbias_detector = CounterfactualBiasDetector()\n\n# detect bias in the model based on the given texts\n# here, clf is a scikit-learn text classification pipeline trained for a binary classification task\ndetection_res = bias_detector.process(\n    texts=texts,\n    predict_func=clf.predict_proba\n)\n\n# see a summary of the detection\ndetection_res.report()\n\n# visualize the counterfactual scores\ndetection_res.visualize_counterfactual_scores(concept="religion", top_n=10)\n```\n\nYou will get results as Boxplots, among others, indicating the impact of keywords and concepts on the prediction of your model.\nExample output:\n![](resources/hatespeech_dl_scores_religion.png)\n\n\nSee more detailed examples in the [tutorial](tutorials/tutorial-toxic-comments/).\n\n\n## Development setup\n\n- First you need to install poetry to manage your python environment: https://python-poetry.org/docs/#installation\n- Run `make install` to install the dependencies and get the spacy basemodels.\n- Now you can use `biaslyze` in your jupyter notebooks.\n\n\n### Adding concepts and keywords\n\nYou can add concepts and new keywords for existing concepts by editing [concepts.py](https://github.com/biaslyze-dev/biaslyze/blob/main/biaslyze/concepts.py).\n\n## Preview/build the documentation with mkdocs\n\nTo preview the documentation run `make doc-preview`. This will launch a preview of the documentation on `http://127.0.0.1:8000/`.\nTo build the documentation html run `make doc`.\n\n\n## Run the automated tests\n\n`make test`\n\n\n## Style guide\n\nWe are using isort and black: `make style`\nFor linting we are running ruff: `make lint`\n\n## Contributing\n\nFollow the google style guide for python: https://google.github.io/styleguide/pyguide.html\n\nThis project uses black, isort and ruff to enforce style. Apply it by running `make style` and `make lint`.\n\n## Acknowledgements\n\n* Funded from March 2023 until August 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)\n',
    'author': 'Tobias Sterbak & Stina Lohmüller',
    'author_email': 'hello@biaslyze.org',
    'maintainer': 'Tobias Sterbak',
    'maintainer_email': 'hello@tobiassterbak.com',
    'url': 'https://biaslyze.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
