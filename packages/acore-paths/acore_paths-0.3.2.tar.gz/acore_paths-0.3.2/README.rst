
.. .. image:: https://readthedocs.org/projects/acore-paths/badge/?version=latest
    :target: https://acore-paths.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_paths-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/acore_paths-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_paths-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_paths-project

.. image:: https://img.shields.io/pypi/v/acore-paths.svg
    :target: https://pypi.python.org/pypi/acore-paths

.. image:: https://img.shields.io/pypi/l/acore-paths.svg
    :target: https://pypi.python.org/pypi/acore-paths

.. image:: https://img.shields.io/pypi/pyversions/acore-paths.svg
    :target: https://pypi.python.org/pypi/acore-paths

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_paths-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_paths-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-paths.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-paths.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_paths-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_paths-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_paths-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-paths#files


Welcome to ``acore_paths`` Documentation
==============================================================================
Azerothcore 魔兽世界服务器上的文件目录结构定义. 你可以直接用 ``import acore_paths.api as acore_paths`` 来 import 这些路径, 并在业务代码中引用这些路径. 每一个路径都是一个 ``pathlib.Path`` 对象, 并且都是绝对路径. 该项目可以作为一个 Python 库供其他项目使用, 从而避免了重复定义目录结构的麻烦, 避免了手写路径时可能出现的错误, 一次发明, 到处使用.

注:

    本项目支持 Python3.4+, 没有任何依赖.

`点击这里 <https://github.com/MacHu-GWU/acore_paths-project/blob/main/acore_paths/acore_paths.py>`_ 查看所有重要路径的定义.

**Usages**

.. code-block:: python

    >>> import acore_paths.api as acore_paths
    >>> acore_paths.dir_...
    >>> acore_paths.path_...


.. _install:

Install
------------------------------------------------------------------------------

``acore_paths`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install acore-paths

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade acore-paths
