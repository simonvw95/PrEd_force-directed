# PrEd

The purpose of the PrEd algorithm is to adjust/improve the layout of existing graph drawings. The algorithm takes as input a graph layout and moves nodes in a force-directed manner, similarly to standard force-directed graph layout algorithms. The key contribution of PrEd is that it respects edge-crossings, no new edge crossings will be created nor will existing edge crossings be removed.

The use of this project is to view the inner workings of the PrEd algorithm with the help of a Graphical User Interface (GUI), where users can visibly see the changes in the layout and manually go back through multiple iterations.

Additionally, note that this is a side-project that has been abandoned. The main project I am working on has a plethora of dependencies issues and over 12 scripts that all rely on each other. For the scope of this course it would be too much.

![alt text](https://github.com/simonvw95/PrEd_force-directed/blob/master/results/figures/gui_example.png "GUI example")

[![DOI](https://sandbox.zenodo.org/badge/463079196.svg)](https://sandbox.zenodo.org/badge/latestdoi/463079196)

The Binder page does not work for now since the code launches a separate window for the GUI, this appears to not be compatible with Binder.
[Interactive code via Binder](https://mybinder.org/v2/gh/simonvw95/PrEd_force-directed/master)

[PrEd algorithm source](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.700.888&rep=rep1&type=pdf#:~:text=Abstract%20PrEd%20%5BBer00%5D%20is%20a,preserving%20its%20edge%20crossing%20properties.&text=The%20algorithm%20ensures%20that%20nodes%20do%20not%20cross%20edges%20during%20its%20execution.)

[Improved algorithm based on PrEd: ImPrEd](https://hal.inria.fr/inria-00605921/document)



# Installing dependencies

### For course participants, only `gui.py` has been modified as a result of the course's teachings.

Start off with getting a local copy of the current repository 
`$ git clone https://github.com/simonvw95/PrEd_force-directed.git`

## Windows
1. Download Python 3.9.7 from [site](https://www.python.org/downloads/).
2. Install ensuring that "Add Python to PATH" and "PIP installation" are enabled.
3. Open Command Prompt and enter the following command
```python -m venv [name_of_virtual_env_without_brackets]```
4. Then in the same terminal activate the virtual environment
```[name_of_virtual_env_without_brackets]\Scripts\activate```
5. Then install the dependencies needed to run the scripts using the requirements.txt file from this repository
```pip install -r requirements.txt```

## Linux
1. Run the following commands
```
$ sudo apt install python3-distutils python3-dev python3-testresources subversion
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
$ python -m venv [name_of_virtual_env_without_brackets]
```
2. Then in the same terminal activate the virtual environment
```source [name_of_virtual_env_without_brackets]/bin/activate```
3. Then install the dependencies needed to run the scripts using the requirements.txt file from this repository
```pip install -r requirements.txt```

## MACOS
1. Open Terminal and enter `python3 --version` to install the interpreter and other command line tools.
2. Run the following commands
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
$ python -m venv [name_of_virtual_env_without_brackets]
```
2. Then in the same terminal activate the virtual environment
```source [name_of_virtual_env_without_brackets]/bin/activate```
3. Then install the dependencies needed to run the scripts using the requirements.txt file from this repository
```pip install -r requirements.txt```




## Using the GUI
In a terminal with the activated virtual environment (with the installed dependencies) write:

`python src/gui.py`

The gui input parameters are required to be non-negative integers, exceptions will be thrown when this is not the case.
If the program does not terminate after quitting the Quit Program button then exit the terminal and start it again.

Version 0.1.0

## Project organization

```
.
├── .gitignore
├── CITATION.md
├── LICENSE.md
├── README.md
├── requirements.txt
├── bin                <- Compiled and external code, ignored by git (PG)
│   └── external       <- Any external source code, ignored by git (RO)
├── config             <- Configuration files (HW)
├── data               <- All project data, ignored by git
│   ├── processed      <- The final, canonical data sets for modeling. (PG)
│   ├── raw            <- The original, immutable data dump. (RO)
│   └── temp           <- Intermediate data that has been transformed. (PG)
├── docs               <- Documentation notebook for users (HW)
│   ├── manuscript     <- Manuscript source, e.g., LaTeX, Markdown, etc. (HW)
│   └── reports        <- Other project reports and notebooks (e.g. Jupyter, .Rmd) (HW)
├── results
│   ├── figures        <- Figures for the manuscript or reports (PG)
│   └── output         <- Other output for the manuscript or reports (PG)
└── src                <- Source code for this project (HW)

```


## License

This project is licensed under the terms of the [MIT License](/LICENSE.md)

## Citation

Please [cite this project as described here](/CITATION.md).
