Contributing
============

How to Contribute
-----------------

There are a lot of different ways to contribute to a project

Filing issues:
^^^^^^^^^^^^^^

If you would like to file an issue this project uses `Github issues`_ for both
feature requests and bugs.

.. _`Github Issues`: https://github.com/hockeybuggy/dataclass_structor/issues


Making code changes:
^^^^^^^^^^^^^^^^^^^^

If you want to make changes to the code start with::

    git clone dataclass_structor
    pipenv install --dev

After you make some changes create a Github pull request. After opening up the
pull request CI (continuous integration) will run some tests. In order for your
PR to be accepted it will need pass the tests, have the correct types, as well
as be formatted "correctly".

To run the tests::

    pipenv run test  # This will run pytest

To check that the types are correct::

    pipenv run typecheck  # This will run mypy

To format the code run::

    pipenv run format  # This will run black


Updating documentation:
^^^^^^^^^^^^^^^^^^^^^^^

If you would like to update documentation::

    git clone dataclass_structor
    pipenv install --dev
    pipenv run build-docs

Code of Conduct
---------------

This project follows and will enforce, the Contributor Covenant:
https://github.com/hockeybuggy/dataclass_structor/CODE_OF_CONDUCT.md
