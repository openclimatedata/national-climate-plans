Data Package with Nationally Determined Contributions (NDCs) and Intended Nationally Determined Contributions (INDCs) as provided in the UNFCCC secreteriat's registries.
Contains only the main document using an English version if multiple are available.

## Data

NDCs are pre-processed in the
NDC Data Package (https://github.com/openclimatedata/ndcs) and INDCs in the
INDC Data Package (https://github.com/openclimatedata/indcs).
This Data Package only contains one document per party, the main NDC or INDC
document. For convenience all documents are copied with unified filenames
in the `pdfs` directory.

## Preparation

Clone this repository with

  git clone https://github.com/openclimatedata/nationally-determined-contributions.git  --recursive

Run

    make

to generate the combined list from the Data Packages mentioned above.

## Requirements

Python3 is used, all dependencies are installed automatically into a Virtualenv
when using the `Makefile`.

## License

The Python files in `scripts` are released under an
[CC0 Public Dedication License](https://creativecommons.org/publicdomain/zero/1.0/).
