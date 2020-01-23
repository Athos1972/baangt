# Integration with ReadTheDocs.io
The aim of this task is to provide automatically generated documentation from source code using ``Sphinx`` so that we
can automatically update [ReadTheDocs](http://readthedocs.io) and docs-pages on [Gogs](https://gogs.earthsquad.global) and later on Github.

Implementation should follow roughly the steps from [this tutorial](https://daler.github.io/sphinxdoc-test/includeme.html).

# DoD:
* Sphinx was configured properly in ``conf.py`` so that generation of extracted documentation from the source code happens
* `index.rst` and *.rst-Files for all relevant paths were built properly (using `sphinx-apidoc ../ --output-dir docs`)
* Necessary GIT-Branch for `gh-pages` was created and `Makefile` updated accordingly.
* Contents of ``README.md`` were transformed into `Readme.rst`, properly formatted and all necessary steps taken to ensure
readability on github pages. 
* Pull request created and result of local test attached to pull request