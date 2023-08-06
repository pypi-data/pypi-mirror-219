# spark_generated_rules_tools

[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)

spark_generated_rules_tools is a Python library that implements quality rules in sandbox

## Installation

The code is packaged for PyPI, so that the installation consists in running:


## Usage

wrapper create hammurabies 

## Sandbox
## Installation
```sh
!yes| pip uninstall spark-generated-rules-tools
```

```sh
pip install spark-generated-rules-tools --user --upgrade
```

## IMPORTS
```sh
import os
import pyspark

from spark_generated_rules_tools import dq_validate_rules

```

## Variables
```sh
user_sandbox="P030772"
```


## Creating Workspace
```sh
dq_path_workspace(user_sandbox=user_sandbox)
```


## Run 
```sh
dq_run_sandbox(spark=spark,
               sc=sc,
               parameter_conf_list=parameter_conf_list,
               url_conf=url_conf)
```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).

## New features v1.0

## BugFix

- choco install visualcpp-build-tools

## Reference

- Jonathan Quiza [github](https://github.com/jonaqp).
- Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
