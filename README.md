# gh-pages-side-by-side-code-examples

Example of creating side-by-side code examples for different languages.  I want to be able to view them in an friendly way using a browser (hence Github Pages).

To view in Github Pages, click on the link below.

<http://tomkraljevic.github.io/gh-pages-side-by-side-code-examples/>

<br>
<hr>

# 1.  Adding a new example

## The generation process

The gen.py tool creates the result examples.html file.
(Look at the trivial Makefile.)

### Tools required to run the generator

* Python (gen.py was developed with Python 2.7)
* npm
* npm's markdown command-line tool

I installed the markdown tool on my Macbook Pro with the following command:

```
npm install markdown-to-html -g
```


### Commands to run

On Macbook Pro:

```
make
git add examples.html
git commit
git push
```

## Top-level directory layout

**README.md**   
This file.

**Makefile**   
Very simple helper for running the generation process.

**./gen.py**  
Tool to generate examples.html.

**examples**  
The example code.  New files generally want to go somewhere in here.

**examples.html**   
Generated from files in the examples directory.

**data**   
Data used by examples.

**index.html**   
What gh-pages points to.

**packages**   
Some helper packages used by the examples (ex package for R).

**static**   
Static resources (jquery, bootstrap, highlight.js).


## Adding a new case for an existing example

Usually this is as easy as just dropping in one more file with the right name that gen.py knows to look for.  You need to add that file in the one specific already-existing example directory.

Unless you want to add a totally new kind of example, in which case read on...


## Adding a new kind of example (i.e. language type)

gen.py has the following three arrays.  (The names are named weirdly to satisfy PEP-8 and still visually line up nicely.)

```
    _lang__________ = ["lang-r", "lang-r"]
    _tabs_to_check_ = ["R",      "h2o-R"]
    _files_to_check = ["ex-R.R", "ex-h2o.R"]
```

Adding a new kind of example means adding an element to each of these arrays.

* The lang array is the name of the language according to highlight.js.
* The tabs array is the name of the tab as seen by the user.
* The files array is the name of the file checked for by gen.py.


## Adding a new example

* Create a new directory.  The name of the directory is not used for any of the generated output.

* Add your new directory to the idx file of the category that contains it.

* Add a ex.txt file in your new directory.  This is one line that contains the example name.

* Add a ex.md file in your new directory.  This is a markdown file that describes the example.  For consistency with the generated code from gen.py, this should not include H1, H2 or H3 tags.  This may include H4, H5, H6 tags.

* The example description markdown file ex.md is converted to html using the node **markdown** tool.

* Create a single code file for each kind of example you want to provide.
  * ex-R.R
  * ex-h2o.R
  * ... etc.

* Code example files are copied verbatim into the generated examples.html.

> The names of the code example files must match exactly what gen.py expects.

### Finding data files

The ex R package has a locate function which you may find helpful.


## Adding a new category (or subcategory)

* Create a new directory.  The name of the directory is not used for any of the generated output.

* Add your new directory to the idx file of the category that contains it.

* Add a cat.txt file in your new directory.  This is one line that contains the category name.

* Add an idx file in your new directory.  idx is a multi line file.  each line contains the name of a directory.  each directory is either a sub-category or an example.  items appear in the order they are included in the idx file.

* Note that the top-level category (Data Science Examples) is special and generally ignored by gen.py so that "Data Science Examples" isn't repeated all over the place.


<br>
<hr>

# 2. Testing

Testing will be driven by a jenkins job that makes some assumptions.

* Assumption:  H2O can run anywhere (in terms of cwd) on the local machine.  The test must provide an absolute path to h2o.  (This is why the "locate" methods is useful.)
* Assumption:  H2O is running with 1 node on the local machine.  It will be started ahead of time.  h2o.init() will work and find an h2o.
* Assumption:  H2O will be started with -Xmx5g.
* Assumption:  Each example has a fresh H2O with no keys in the K/V store.
* Assumption:  Tests can be run in any order.
* Assumption:  The test itself will be started with the cwd that the test file lives in.
* Assumption:  The ex package will be installed when R is run.
* Assumption:  The H2O package will be installed when R is run.

Other do's and dont's:

* Examples should not call h2o.shutdown().
* H2O R tests will be run via:
  *  R -f ex-h2o.R

## How to locally build and install the ex R package

I did this with RStudio...  Need better instructions here.
