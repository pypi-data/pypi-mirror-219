# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replay',
 'replay.metrics',
 'replay.models',
 'replay.scenarios',
 'replay.scenarios.two_stages',
 'replay.spark_custom_models',
 'replay.splitters']

package_data = \
{'': ['*']}

install_requires = \
['d3rlpy',
 'gym==0.17.2',
 'implicit>=0.5',
 'lightautoml>=0.3.1,<0.3.7',
 'lightfm',
 'llvmlite>=0.32.1',
 'numba>=0.50',
 'numpy>=1.20.0',
 'optuna',
 'pandas',
 'poetry-core==1.6.0',
 'psutil',
 'pyarrow',
 'pyspark>=3.0,<3.2',
 'pytorch-ranger>=0.1.1,<0.2.0',
 'scikit-learn',
 'scipy',
 'seaborn',
 'torch']

setup_kwargs = {
    'name': 'replay-rec',
    'version': '0.11.0',
    'description': 'RecSys Library',
    'long_description': '# RePlay\n\nRePlay is a library providing tools for all stages of creating a recommendation system, from data preprocessing to model evaluation and comparison.\n\nRePlay uses PySpark to handle big data.\n\nYou can\n\n- Filter and split data\n- Train models\n- Optimize hyper parameters\n- Evaluate predictions with metrics\n- Combine predictions from different models\n- Create a two-level model\n\nDocumentation is available [here](https://sb-ai-lab.github.io/RePlay/).\n\n<a name="toc"></a>\n# Table of Contents\n\n* [Installation](#installation)\n* [Quickstart](#quickstart)\n* [Resources](#examples)\n* [Contributing to RePlay](#contributing)\n\n\n<a name="installation"></a>\n## Installation\n\nUse Linux machine with Python 3.7-3.9, Java 8+ and C++ compiler.\n\n```bash\npip install replay-rec\n```\n\nTo get the latest development version or RePlay, [install it from the GitHab repository](https://sb-ai-lab.github.io/RePlay/pages/installation.html#development).\nIt is preferable to use a virtual environment for your installation.\n\nIf you encounter an error during RePlay installation, check the [troubleshooting](https://sb-ai-lab.github.io/RePlay/pages/installation.html#troubleshooting) guide.\n\n\n<a name="quickstart"></a>\n## Quickstart\n\n```python\nfrom rs_datasets import MovieLens\n\nfrom replay.data_preparator import DataPreparator, Indexer\nfrom replay.metrics import HitRate, NDCG\nfrom replay.models import ItemKNN\nfrom replay.session_handler import State\nfrom replay.splitters import UserSplitter\n\nspark = State().session\n\nml_1m = MovieLens("1m")\n\n# data preprocessing\npreparator = DataPreparator()\nlog = preparator.transform(\n    columns_mapping={\n        \'user_id\': \'user_id\',\n        \'item_id\': \'item_id\',\n        \'relevance\': \'rating\',\n        \'timestamp\': \'timestamp\'\n    }, \n    data=ml_1m.ratings\n)\nindexer = Indexer(user_col=\'user_id\', item_col=\'item_id\')\nindexer.fit(users=log.select(\'user_id\'), items=log.select(\'item_id\'))\nlog_replay = indexer.transform(df=log)\n\n# data splitting\nuser_splitter = UserSplitter(\n    item_test_size=10,\n    user_test_size=500,\n    drop_cold_items=True,\n    drop_cold_users=True,\n    shuffle=True,\n    seed=42,\n)\ntrain, test = user_splitter.split(log_replay)\n\n# model training\nmodel = ItemKNN()\nmodel.fit(train)\n\n# model inference\nrecs = model.predict(\n    log=train,\n    k=K,\n    users=test.select(\'user_idx\').distinct(),\n    filter_seen_items=True,\n)\n\n# model evaluation\nmetrics = Experiment(test,  {NDCG(): K, HitRate(): K})\nmetrics.add_result("knn", recs)\n```\n\n<a name="examples"></a>\n## Resources\n\n### Usage examples\n1. [01_replay_basics.ipynb](https://github.com/sb-ai-lab/RePlay/blob/main/experiments/01_replay_basics.ipynb) - get started with RePlay.\n2. [02_models_comparison.ipynb](https://github.com/sb-ai-lab/RePlay/blob/main/experiments/02_models_comparison.ipynb) - reproducible models comparison on [MovieLens-1M dataset](https://grouplens.org/datasets/movielens/1m/).\n3. [03_features_preprocessing_and_lightFM.ipynb](https://github.com/sb-ai-lab/RePlay/blob/main/experiments/03_features_preprocessing_and_lightFM.ipynb) - LightFM example with pyspark for feature preprocessing.\n3. [04_splitters.ipynb](https://github.com/sb-ai-lab/RePlay/blob/main/experiments/04_splitters.ipynb) - An example of using RePlay data splitters.\n3. [05_feature_generators.ipynb](https://github.com/sb-ai-lab/RePlay/blob/main/experiments/05_feature_generators.ipynb) - Feature generation with RePlay.\n\n\n### Videos and papers\n* **Video guides**:\n\t- [Replay for offline recommendations, AI Journey 2021](https://www.youtube.com/watch?v=ejQZKGAG0xs)\n\n* **Research papers**:\n\t- Yan-Martin Tamm, Rinchin Damdinov, Alexey Vasilev [Quality Metrics in Recommender Systems: Do We Calculate Metrics Consistently?](https://dl.acm.org/doi/10.1145/3460231.3478848)\n\n<a name="contributing"></a>\n## Contributing to RePlay\n\nWe welcome community contributions. For details please check our [contributing guidelines](CONTRIBUTING.md).\n',
    'author': 'AI Lab',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sb-ai-lab.github.io/RePlay/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
