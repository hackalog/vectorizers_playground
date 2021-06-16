Vectorizers Playground
==============================
_Author: Tutte Institute for Mathematics and Computing_

An Easydata-generated repo for exploring the TIMC vectorizers library to construct word, document and topic embeddings.


GETTING STARTED
---------------
### Initial environment setup

First, create fork and clone your version of the repo. Then create and switch to the virtual environment:
```
cd vectorizers_playground
make create_environment
conda activate vectorizers_playground
```
You're now ready to explore the vectorizers playground notebooks.

**Troubleshooting**: If you have any issues with `make create_environment`, try the following:

* Make note of the path to your conda binary:
```
   $ which conda
   ~/miniconda3/bin/conda
```
* ensure your `CONDA_EXE` environment variable is set to this value (or edit `Makefile.include` directly)
```
    export CONDA_EXE=~/miniconda3/bin/conda
```
* If that doesn't work, see [Setting up and Maintaining your Conda Environment Reproducibly](reference/easydata/conda-environments.md)

### Explore the vectorizers playground
Now you're ready to run `jupyter lab` (or jupyter notebook) and explore the notebooks in the `notebooks` directory.

Here are the current notebooks:

* `01-vectorizers-quickstart`: The *I don't care how it works, show me what to do* approach. Start here to learn how to use the vectorizers library for word, document and topic vectorization and embedding.
* `02-word-embedding`: [WIP] Work in progess comparison of the `vectorizers` library **word embedding** approach. 
* `03-document-embedding`: An explanation of the `vectorizers` library approach to **document embedding**, including a walkthrough and comparison of the various steps against common document embedding algorithms such as USE and BERT.
* `04-topic-embedding`: [WIP] A qualitative comparison of the `vectorizers` approach to **topic embedding**. 
* `00-20-newsgroups-setup`: This notebooks documents the preprocessing and cleanup to the 20 newsgroups dataset that is available via `ds.load('20_newsgroups_pruned')` and used in the other notebooks.


ABOUT EASYDATA
--------------
This git repository is build from the [Easydata](https://github.com/hackalog/easydata) framework, which aims to make
your data science workflow reproducible. The Easydata framework includes:

* tools for managing conda environments in a consistent and reproducible way,
* built-in dataset management (including tracking of metadata such as LICENSES and READMEs),
* a prescribed project directory structure,
* workflows and conventions for contributing notebooks and other code.

### Easydata References
* [Setting up and Maintaining your Conda Environment Reproducibly](reference/easydata/conda-environments.md)
* [Getting and Using Datasets](reference/easydata/datasets.md)
* [Using Notebooks for Analysis](reference/easydata/notebooks.md)
* [Sharing your Work](reference/easydata/sharing-your-work.md)


EASYDATA REQUIREMENTS
------------
* Make
* conda >= 4.8 (via Anaconda or Miniconda)
* Git

Project Organization
------------
* `LICENSE`
* `Makefile`
    * Top-level makefile. Type `make` for a list of valid commands.
* `Makefile.include`
    * Global includes for makefile routines. Included by `Makefile`.
* `Makefile.env`
    * Command for maintaining reproducible conda environment. Included by `Makefile`.
* `README.md`
    * this file
* `catalog`
  * Data catalog. This is where config information such as data sources
    and data transformations are saved.
  * `catalog/config.ini`
     * Local Data Store. This configuration file is for local data only, and is never checked into the repo.
* `data`
    * Data directory. Often symlinked to a filesystem with lots of space.
    * `data/raw`
        * Raw (immutable) hash-verified downloads.
    * `data/interim`
        * Extracted and interim data representations.
    * `data/interim/cache`
        * Dataset cache
    * `data/processed`
        * The final, canonical data sets ready for analysis.
* `docs`
    * Sphinx-format documentation files for this project.
    * `docs/Makefile`: Makefile for generating HTML/Latex/other formats from Sphinx-format documentation.
* `notebooks`
    *  Jupyter notebooks. Naming convention is a number (for ordering),
    the creator's initials, and a short `-` delimited description,
    e.g. `1.0-jqp-initial-data-exploration`.
* `reference`
    * Data dictionaries, documentation, manuals, scripts, papers, or other explanatory materials.
    * `reference/easydata`: Easydata framework and workflow documentation.
    * `reference/templates`: Templates and code snippets for Jupyter
    * `reference/dataset`: resources related to datasets; e.g. dataset creation notebooks and scripts
* `reports`
    * Generated analysis as HTML, PDF, LaTeX, etc.
    * `reports/figures`
        * Generated graphics and figures to be used in reporting.
* `environment.yml`
    * The user-readable YAML file for reproducing the conda/pip environment.
* `environment.(platform).lock.yml`
    * resolved versions, result of processing `environment.yml`
* `setup.py`
    * Turns contents of `src` into a
    pip-installable python module  (`pip install -e .`) so it can be
    imported in python code.
* `src`
    * Source code for use in this project.
    * `src/__init__.py`
        * Makes `src` a Python module.
    * `src/data`
        * Scripts to fetch or generate data.
    * `src/analysis`
        * Scripts to turn datasets into output products.

--------

<p><small>This project was built using <a target="_blank" href="https://github.com/hackalog/easydata">Easydata</a>, a python framework aimed at making your data science workflow reproducible.</small></p>
