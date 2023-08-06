# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stitchnet',
 'stitchnet.ensemble',
 'stitchnet.finetuning',
 'stitchnet.plot',
 'stitchnet.stitchonnx']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.13.1,<3.0.0',
 'evaluate>=0.4.0,<0.5.0',
 'graphviz>=0.20.1,<0.21.0',
 'netron>=7.0.4,<8.0.0',
 'numpy>=1.23.1,<2.0.0',
 'onnx-tool==0.7.3',
 'onnx2torch>=1.4.1,<2.0.0',
 'onnx==1.13.1',
 'onnxoptimizer>=0.3.0,<0.4.0',
 'onnxruntime>=1.12.1,<2.0.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'pyre-extensions>=0.0.30,<0.0.31',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'skl2onnx>=1.12.0,<1.13.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'transformers>=4.25.1,<5.0.0']

setup_kwargs = {
    'name': 'stitchnet',
    'version': '0.2.0',
    'description': '',
    'long_description': 'StitchNet: Composing Neural Networks from Pre-Trained Fragments\n=============\n\n\nInstallation\n=============\n\n    pip install stitchnet\n    \nUsage\n=============\n    \n    import stitchnet\n    \n    # prepare stitching data D\n    from stitchnet import load_hf_dataset\n    # load the beans dataset from huggingface\n    dataset_train, dataset_val = load_hf_dataset(\'beans\', train_split=\'validation\', val_split=\'test\', label_column=\'labels\', seed=47)\n    \n    # generate stitchnets\n    import numpy as np\n    from tqdm import tqdm\n    stitching_dataset = np.vstack([x[\'pixel_values\'] for x in tqdm(dataset_train.select(range(32)))])\n    score,net = generate(stitching_dataset, threshold=0.8, totalThreshold=0, maxDepth=10, K=2, sample=True)\n    \n    # print macs and params\n    net.get_macs_params() # {\'macs\': 4488343528.0, \'params\': 25653096}\n    \n    # save onnx\n    net.save_onnx(\'./_data/net\') # saving to ./_results/net.onnx\n        \n    # draw the stitchnet\n    net.draw_svg(\'./_data/net\') # saving to ./_results/net.svg\n    \n    # train a classifier\n    net.fit(dataset_train, label_column="labels")\n    \n    # use it for prediction\n    net.predict_files([\'./_results/test.jpg\']) # [{\'score\': [0.8, 0.2, 0.0], \'label\': 0}]\n    \n    # evaluate with validation dataset\n    net.evaluate_dataset(dataset_val, label_column=\'labels\') # {\'accuracy\': 0.7421875}\n\nCUDA\n=============\nSee https://pytorch.org/get-started/previous-versions/ to install appropriate version. For example\n\n    # CUDA 11.6\n    pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116\n\n\nExperiment Notebooks\n=============\n\n1. Download dogs and cats dataset from https://www.kaggle.com/c/dogs-vs-cats/data and put train data in _data/dogs_cats/raw/train folder\n2. See 00_prepare_data.ipynb to split the images into cats and dogs folder\n3. See 01_download_networks.ipynb to download the pretrained networks from Torchvision\n4. See 02_generate_fragments.ipynb to generate fragments from the pretrained networks\n5. See 03_stitchnet.ipynb to generate stitchnets\n6. See 04_render_graph.ipynb to create svg images of the network graphs using netron\n7. See 05_eval_original_networks.ipynb for evaluating the original pretrained networks\n8. See 06_finetuning.ipynb to generate the finetuning result\n9. See 07_ensemble.ipynb to generate the ensemble result\n10. See 08_number_of_samples_for_stitching.ipynb for experimenting with varying number of samples to use when stitching\n11. See 09_plot_results.ipynb plot figures of the results for the paper\n\n\nInstallation using conda\n=============\n\nCreate a new conda env\n\n    conda create -n stitchnet python=3.10\n    \nActivate stitchnet conda env\n\n    conda activate stitchnet\n\nFor conda and NVIDIA gpu, please also install for CUDA runtime on onnx\n\n    conda install -c conda-forge cudnn\n    \nInstall poetry\n\n    curl -sSL https://install.python-poetry.org | python3 -\n\nInstall dependencies using poetry \n\n    poetry install\n\n',
    'author': 'Surat Teerapittayanon',
    'author_email': 'steerapi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
