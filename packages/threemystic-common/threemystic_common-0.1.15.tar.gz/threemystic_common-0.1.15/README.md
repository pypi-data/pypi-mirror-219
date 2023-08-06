# 3mystic_common
A set of common files that are used for the various projects under 3 Mystic Apes

This project is currently in beta, along with the other projects. Once the other projects come out of beta this one will as well. However, this is also, the most stable of the project. I am trying not to change things that would break from version to version. So if you would like to use something here, it should be relatively safe. I will try to call out breaking changes.

# Install

## pip

The latest version of this project is currently being pushed to
https://pypi.org/project/threemystic-common/

pip install threemystic-common

If you would prefer to install directly from GitHub you need to install Hatch.
Please refer to the section below for that.

Once hatch is installed you can use pip

pip install https://github.com/3MysticApes/3mystic_common



## Hatch
This project is packaged using Hatch. If you need to install Hatch please refer to their documentation
https://hatch.pypa.io/latest/install/

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