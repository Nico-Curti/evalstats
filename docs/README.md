# Create Sphinx documentation

To run the sphinx auto-documentation, first of all we need to install the package using the command:

```bash
python -m pip install sphinx
```

Then, according to the online documentation (ref. [here](https://www.sphinx-doc.org/en/master/usage/quickstart.html)), we can initialize the documentation folder using the built-in python entry-point

```bash
sphinx-quickstart
```

The command will ask you to insert some information (as input command during the setup procedure), obtaining an output as:

```bash
Welcome to the Sphinx 5.1.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: evalstats
> Author name(s): Nico Curti
> Project release []: 0.0.1

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]: en

Creating file /mnt/c/Users/utente/Code/evalstats/docs/source/conf.py.
Creating file /mnt/c/Users/utente/Code/evalstats/docs/source/index.rst.
Creating file /mnt/c/Users/utente/Code/evalstats/docs/Makefile.
Creating file /mnt/c/Users/utente/Code/evalstats/docs/make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file /mnt/c/Users/utente/Code/evalstats/docs/source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

Now you can customize your `conf.py` script according to your needs (eg. ref. [here](https://github.com/Nico-Curti/blob/main/docs/source/conf.py)) and create the correct set of Rst files for the autodoc of Python doc-strings (eg. ref. [here](https://github.com/Nico-Curti/blob/main/docs/source/index.rst))

At the end of your configuration you can generate the entire documentation running the command:

```bash
make html
```

inside the `/docs/` folder.
