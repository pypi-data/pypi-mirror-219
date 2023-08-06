# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noiseflow',
 'noiseflow.cc',
 'noiseflow.cc.python',
 'noiseflow.client',
 'noiseflow.config',
 'noiseflow.signal',
 'noiseflow.signal.python',
 'noiseflow.tests',
 'noiseflow.utils']

package_data = \
{'': ['*'],
 'noiseflow.cc': ['include/*', 'src/*'],
 'noiseflow.signal': ['include/*', 'src/*']}

install_requires = \
['faker>=18.13.0,<19.0.0',
 'h5py>=3.7.0,<4.0.0',
 'joblib>=1.3.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.25.0,<2.0.0',
 'obspy>=1.4.0,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'noiseflow',
    'version': '0.0.9',
    'description': 'An ambient noise package',
    'long_description': '# NoiseFlow\n\n\n[![Actions Status](https://github.com/shakeflow/noiseflow/actions/workflows/workflow.yml/badge.svg)](https://github.com/shakeflow/noiseflow/actions)\n[![coverage](https://codecov.io/gh/shakeflow/noiseflow/branch/main/graph/badge.svg)](https://codecov.io/gh/shakeflow/noiseflow)\n[![docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://shakeflow.github.io/noiseflow/)\n[![supported versions](https://img.shields.io/pypi/pyversions/noiseflow.svg?label=python_versions)](https://pypi.python.org/pypi/noiseflow)\n[![docs](https://badge.fury.io/py/noiseflow.svg)](https://badge.fury.io/py/noiseflow)\n\n\n## Prerequisites\n\nNoiseFlow now supports `Clang` and `GCC` compiler in MacOS and Linux system separately, and all installation processes are under the `conda` environment, and we recommend to use miniconda. Make sure to install the following pre-packages before installing noiseflow:\n\n\nIf you use `Clang` in Mac, please install `OpenMP` via `brew` as following:\n\n```bash\nbrew install openmp\n```\n\nAnd use `pip` and `conda` to install the following packages:\n\n```bash\npip install joblib\n\nconda install -c conda-forge numpy scipy matplotlib \nconda install -c conda-forge obspy\nconda install -c conda-forge fftw (动态库)\nconda install -c conda-forge pybind11 (头文件)\nconda install -c conda-forge xtensor xsimd xtl xtensor-blas xtensor-python (可能是静态库)\nconda install -c conda-forge xtensor-fftw  #(usually failed at most time)  \n```\n\nThe `xtensor-fftw` and `KFR` need to be installed from source, first download them:\n\n\n```bash\ngit clone https://github.com/OUCyf/noiseflow.git\ncd noiseflow\ngit submodule init\ngit submodule update\n```\n\n\n\nNote the `xtensor-fftw` do not support M1 chip, and if it is failed to install via conda, you can install it from source into conda environment as `$CONDA_PREFIX`\n\n```bash\ncd ./external/xtensor-fftw\nmkdir build && cd build\ncmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX\nmake install\n```\n\n\n\nThe `KFR` package is C++ DSP framework, should be installed in `./extern/kfr` from source\n\n```bash\ncd ./external/kfr\nmkdir build && cd build\ncmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX\nmake install\n```\n\n\n\n\n## Installation\n\nNow you can install `NoiseFlow`. If you use `MacOS`, please make sure to use Clang as the complier\n\n```bash\nexport CXX=clang++\n# unset CXX\npython setup.py install\n```\n\nIf you use `Linux`, please use GCC as the compiler\n\n```bash\nexport CXX=g++-13\npython setup.py install\n```\n\n\nIf you use `HPC` with `module` tool, you can use both Clang and GCC, for example using NOTS in Rice University.\n\n```bash\n# use gcc\nmodule load GCC/13.1.0\nexport CXX=g++\npython setup.py install\nINCLUDE_CMAKE_EXTENSION=1 pip install .\n\n# use clang\nmodule load GCCcore/11.2.0\nmodule load Clang/13.0.1\nexport CXX=clang++\npython setup.py install\n```\n\n```bash\nconda install -c conda-forge stockwell\n\nNOISEFLOW_USE_CPP=1 pip install --no-binary :all: noiseflow --no-cache-dir\n\ngit submodule add https://gitclone.com/github.com/kfrlib/kfr.git extern/kfr\n```\nw\n\n\n## License\nNoiseflow is dual-licensed, available under both commercial and apache license.\n\nIf you want to use noiseflow in a commercial product or a closed-source project, you need to purchase a Commercial License.\n\n\n\n`stockwell`: \'numpy>=1.18\', scipy, fftw, [\'cp36-*\', \'cp37-*\', \'cp38-*\', \'cp39-*\', \'cp310-*\']\n\n\n\n## INSTALL (NOETS)\n- conda:\n\n\n\n```bash\nbrew install fftw\nconda install -c conda-forge fftw(没用)\nconda install -c conda-forge pybind11 (头文件)\nconda install -c conda-forge xtensor xsimd xtl xtensor-blas xtensor-python (可能是静态库)\n```\n\n\n\n\n```bash\ncd ./external/xtensor-fftw\nmkdir build && cd build\n\nmyenv = $(conda env list | grep \' \\* \' | awk \'{print $1}\')\nconda_prefix = $(conda info --base)\nexport CMAKE_PREFIX_PATH="${conda_prefix}/envs/${myenv}"\n\n\ncmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCMAKE_PREFIX_PATH=$CONDA_PREFIX\nmake install\n```\n\n\n\n### [build-system]\ncmake = \'^3.18.0\'\nfftw = \'^3.3.10\'\npybind11 = \'^2.10.4\'\nxtensor = \'^0.24.6\'\nxsimd = \'8.0.5\' # when the version is larger than 8.0.5, it will got error in compiling stage.\nxtl = \'^0.7.5\'\nxtensor_blas = \'^0.20.0\'\nxtensor_python = \'^0.26.1\'\nxtensor_fftw = \'^0.2.6\' # not show in conda env\nkfr = \'^5.0.2\' # not show in conda env\n\n### [optional-for-mac]\nlibomp = \'^16.0.6\' # via brew',
    'author': 'Fu Yin',
    'author_email': 'oucyinfu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
