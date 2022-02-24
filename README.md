# PrEd

Version 0.1.0

A Force-Directed algorithm that respects edge-crossings

Source:
https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.700.888&rep=rep1&type=pdf#:~:text=Abstract%20PrEd%20%5BBer00%5D%20is%20a,preserving%20its%20edge%20crossing%20properties.&text=The%20algorithm%20ensures%20that%20nodes%20do%20not%20cross%20edges%20during%20its%20execution.


## Installing dependencies
In a terminal with pip installed run the following command to create a virtual environment
`python -m venv [name_of_virtual_env_without_brackets]`

Then in the same terminal activate the virtual environment

For Mac OS / Linux:
`source [name_of_virtual_env_without_brackets]/bin/activate`

For Windows
`[name_of_virtual_env_without_brackets]\Scripts\activate`

Then install the dependencies needed to run the scripts
`pip install -r requirements.txt`

## Using the GUI
In a terminal with the activated virtual environment (with the installed dependencies) write:

`python gui.py`

If the program does not terminate after quitting the Quit Program button then exit the terminal and start it again.

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
