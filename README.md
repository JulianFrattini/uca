# Use Case Adoption: Case Study Replication Package

[![GitHub](https://img.shields.io/github/license/JulianFrattini/uca)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15672950.svg)](https://doi.org/10.5281/zenodo.15672950)

This repository contains the replication package for the case study on **use case adoption** at a large, globally-distributed company.
In this study, we investigate three research questions:

- RQ1: How are use case descriptions adopted at the case company?
- RQ2: How does use case description quality impact the subsequent development process?
- RQ3: Which requirements engineering factors influence the use case quality?

RQ1 is of descriptive nature, RQ2 and RQ3 of inferential nature.
This repository contains the material to replicate a study with all three research questions.

> [!info]
> Note that the case study that this replication package accompanies uses sensitive data which **cannot be shared**. However, we provide mocked data to make our code and scripts executable.

## Summary of Artifact

This artifact contains the material to replicate the study titled "Adopting Use Case Descriptions for Requirements Specification: an Industrial Case Study" published at the [33rd Requirements Engineering Conference](https://conf.researchr.org/home/RE-2025).
The package consists of data extraction and transformation guidelines, the collected (and anonymized) data, as well as our data visualization and analysis scripts.

## Author Information

This work was produced by the following authors:

| Name | Affiliation | Contact |
|---|---|---|
| Julian Frattini\* | Chalmers University of Technology and University of Gothenburg, Sweden | julian.frattini@chalmers.se |
| Anja Frattini | FernUniversität in Hagen, Germany | |

\* corresponding author

*Cite this article as*: Frattini, J., & Frattini, A. (2025, September). Adopting Use Case Descriptions for Requirements Specification: an Industrial Case Study. In 2025 IEEE 33rd International Requirements Engineering Conference (RE). IEEE.

```bibtex
@inproceedings{frattini2025adopting,
  title={Adopting Use Case Descriptions for Requirements Specification: an Industrial Case Study},
  author={Frattini, Julian and Frattini, Anja},
  booktitle={2025 IEEE 33rd International Requirements Engineering Conference (RE)},
  year={2025},
  organization={IEEE}
}
```

You can use the `CITATION.cff` file to generate an appropriate citation from GitHub directly.

## Artifact Location

The artifact is permanently archived at https://doi.org/10.5281/zenodo.15672950 and available for collaboration at https://github.com/JulianFrattini/uca.

## Description of Artifact

This repository contains the following files.

```
├── data : directory containing data to the extent that it can be shared
│   ├── extraction : data extracted from the collected requirements
│   │   └── uca-automatic.csv : result of executing the eval_scenarios.py script
│   ├── output : data produced by the preparation steps and ready for analysis
│   │   ├── reqs-mocked.csv : an overview of the mocked requirements
│   │   ├── uca-aggregated.csv : a data set consisting of mocked requirements attributes
│   │   └── uca-annotations.csv : a data set consisting of mocked use case annotations
│   └── transformation : directory of (mocked) use cases transformed into sequence diagrams
├── documentation : directory for documentation and guidelines
│   ├── extraction-guidelines.docx : guidelines for the manual extraction of data
│   └── transformation-rules.md : guidelines for the transformation of textual UC descriptions into sequence diagrams
├── figures : directory for all figures
│   ├── descriptive : directory containing figures from the data visualization scripts
│   └── inferential : directory containing figures from the data analysis scripts
├── graphs : directory for all supplementary graphs
│   ├── dag-adoption.graphml : manually generated causal DAG for the analysis of the adoption effect
│   └── rq-mapping.graphml : graph visualizing the three RQs in their context
├── src : directory for all source code
│   ├── analysis : source code pertaining to the actual data analysis
│   │   ├── inferences : directory containing all inferential Bayesian data analyses
│   │   │   ├── cause-analysis : directory containing all analyses for RQ3
│   │   │   └── effect-analysis : directory containing all analyses for RQ2
│   │   ├── util : directory for utility scripts
│   │   │   ├── mocking-annotations.Rmd : script that produces the mocked uca-annotations.csv file
│   │   │   └── mocking-full.Rmd : script that produces the mocked uca-aggregated.csv file
│   │   └── visualization : directory for descriptive data analyses for RQ1
│   │       ├── visualization-annotations.Rmd : visualization of the uca-annotations.csv file
│   │       └── visualization-full.Rnd : visualization of the uca-aggregated.csv file
│   └── processing : source code pertaining to the preparation of the data for analysis
│       ├── structure : dataclass files specifying a mermaid-based sequence diagram
│       ├── util : utility scripts
│       ├── eval_scenarios.py : main script to parse and evaluate use cases specified as sequence diagrams
│       └── requirements.txt : list of required Python libraries
└── README.md : repository overview and usage instructions.
```

Keep in mind that the anonymization and de-sensitivization of the material required removing several pieces of information.
For example, the extraction guidelines do not contain any sensitive terminology or examples.
However, we provide mocked examples of data (e.g., in *data/transformation* or *data/output*) to allow executing the provided scripts.

## System Requirements and Installation Instructions

To view `.md` Markdown files contained in this repository, consider a Markdown viewer like the one [integrated into Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown).
To display and edit graphs specified in `.graphml` format, use a graph editor like [yEd](https://www.yworks.com/products/yed) by yworks.

### Python Scripts

Ensure that you have [Python 3.10](https://www.python.org/downloads/release/python-3100/) and [pip](https://pypi.org/project/pip/) installed on your system. Then, navigate into the *src/processing* directory and install the required libraries via `pip install -r requirements.txt`.

### R Scripts

To run the scripts producing the descriptive statistics (i.e., the data visualization), you need to install [R](https://cran.r-project.org/) (recommended: version 4.4.1) and install the [tidyverse](https://www.tidyverse.org/) packages via `install.packages("tidyverse")`.

To run the scripts performing the inferential statistics (i.e., the causal analyses), you will need to perform the following, additional steps:

1. Install the C toolchain by following the instructions for [Windows](https://github.com/stan-dev/rstan/wiki/Configuring-C---Toolchain-for-Windows#r40), [Mac OS](https://github.com/stan-dev/rstan/wiki/Configuring-C---Toolchain-for-Mac), or [Linux](https://github.com/stan-dev/rstan/wiki/Configuring-C-Toolchain-for-Linux) respectively.
2. Restart RStudio and follow the instructions starting with the [Installation of RStan](https://github.com/stan-dev/rstan/wiki/RStan-Getting-Started#installation-of-rstan)
3. Install the latest version of `stan` by running the following commands
```
    install.packages("devtools")
    devtools::install_github("stan-dev/cmdstanr")
    cmdstanr::install_cmdstan()
```
4. Install all required packages via `install.packages(c("tidyverse", "brms", "ggdag"))` to set up the main libraries.
5. Create a folder called *fits* within *src/analysis* such that `brms` has a location to place all Bayesian models.

## Usage Instructions and Steps to Reproduce

The following instructions guide the usage of the provided artifacts.
For this replication package, this conincides with the necessary steps to reproduce the results reported in our manuscript.

### Data Processing Script

The data processing script `eval_scenarios.py` automatically parses use cases specified as sequence diagrams and evaluates some of their properties (e.g., how many actors and interactions it contains).
To utilize the data processing script, ensure that the [Python-related requirements](#python-scripts) are fulfilled, and navigate a terminal into the folder *src/processing*.
Then execute one of the following commands:

- `python eval_scenarios.py --req <requirement ID> --ucid <use case ID>` to parse a single use case specified by a requirement ID (e.g., `REQ-0001`) and use case ID (e.g., `uc1`) contained in the *data/transformation* directory.
- `python eval_scenarios.py` to parse all use cases in the *data/transformation* directory, evaluate them, and store the evaluations in the [data/extraction/uca-automatic.csv](./data/extraction/uca-automatic.csv) file.

We provide exemplary use cases specified as sequence diagrams in the *data/transformation* folder to allow executing the scripts.

### Data Visualization Scripts

The data visualization scripts contained in *src/analysis/visualization* are Rmarkdown (`.Rmd`) files that require R and the `tidyverse` library.
Once you followed the initial part of the [R setup](#r-scripts), open the visualization files in an IDE of your choice (e.g., VS Code or RStudio) and execute them cell by cell.

> [!warning]
> Note that the *figures* directory contains the figures generated from the real data.
> We commented out all `ggplot2::ggsave` commands that would save a figure to the disk from the visualization scripts as they would overwrite the real figures with ones generated from the provided mocked data.

### Data Analysis Scripts

The data analysis scripts contained in *src/analysis/inferences* are Rmarkdown (`.Rmd`) files that require the full [R setup](#r-scripts) described above.
Open the analysis files in an IDE of your choice (e.g., VS Code or RStudio) and execute them cell by cell.

> [!info]
> Note that the training of Bayesian models with `brms` may take up to a few minutes per model. 

## License

Copyright © 2025 Julian Frattini.
This repository is available under the [MIT license](./LICENSE.md).
