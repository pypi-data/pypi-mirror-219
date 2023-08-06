# 3mystic_cloud_cmdb
A Lightweight Multi Cloud CMDB (Configuration management database)
Currently supports AWS/Azure

The goal of this project is to help you manage the inventory and some base configuration around them. You cannot manage and secure resources you do not know about.

This project is currently in beta, along with the other projects. Once the other projects come out of beta this one will as well. However, this is also, the most stable of the project. I am trying not to change things that would break from version to version. So if you would like to use something here, it should be relatively safe. I will try to call out breaking changes. The connection for both AWS and Azure does currently work. So if you have issues please create an issue.

While in beta not all datasets might be working.

# Install

## pip

The latest version of this project is currently being pushed to
https://pypi.org/project/threemystic-cloud-cmdb/

pip install threemystic-cloud-cmdb

If you would prefer to install directly from GitHub you need to install Hatch.
Please refer to the section below for that.

Once hatch is installed you can use pip

pip install https://github.com/3MysticApes/3mystic_cloud_cmdb

## Hatch
This project is packaged using Hatch. If you need to install Hatch please refer to their documentation
https://hatch.pypa.io/latest/install/

# Setup

Once installed please run 
3mystic_cloud_cmdb -c

# Usage

usage: 3mystic_cloud_cmdb [-h] [-v] [--version] [--config] [--generate] [--provider {aws,azure}]

One Action is required

options:</br>
  -h, --help            show this help message and exit</br>
  -v, --verbose         Verbose output</br>
  --version             Action: outputs the versions of the app being used.</br>
  --config, -c          Action: This is so you can setup the data client</br>
  --data, -d            Action: Pull the various Data from the provider</br>
  --provider {aws,azure}, -p {aws,azure} Provider: This is to set the provider that should be used</br>

The --provider/-p is only reqired if you do not set a default provider with the config.

To see the various data options you can run 
3mystic_cloud_data_client --generate/-g

That will list all current options for pulling datasets for. 

# Contribute
You need to install Hatch. Please see the previous Hatch section under install.

Once you download the project you can do the following
You should be able to run the following command in the root directory for a general status
hatch status

Then from the root directory you can run
pip install ./

I would suggest while you are debugging issues to install it with the command below. Once you are done with your development you can uninstall. This allows you to make edits and test easier.
pip install -e ./
https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-e

