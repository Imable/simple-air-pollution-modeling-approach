# SAPMA: Simple Air Pollution Modelling Approach

## Prerequisites
- This repository cloned to your local machine.
- Python 3.8(.1) installed on your system.
    - Other version should also work, but this requires changing the Python version in the Pipfile in the root of the project.
- The `Tkinter` Python package.
    - This is installed in Python by default.
    - If it is missing from your system, modify your Python installation and select it in the installer.
- `pipenv` installed on your system.
    - Do so by running `pip install pipenv`.
- A folder named `input` in the root of the folder containing the `.xlsx` files with measurements, source data and ship specific data.

## Caveats
- Parsing of JSON lists (e.g. the arguments `--station` and `--weather_plot`) is working differently in CMD and PowerShell. When experiencing the error below change the format of the arguments mentioned above like so.
    - PowerShell: `'[\"ARG_HERE\"]'`
    - CMD: `[\"ARG_HERE\"]`

```
raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)
```
- The `.xslx` file containing ship specific data **has** to be called `ship_specific_data.xlsx` and cannot be renamed using arguments. This file must be placed in the same `/input/` folder as the other input files.
- The `date` columns in the `.xlsx` files **must** be renamed to `DATE` in order for the program to parse them correctly.
- Currently it is recommended to only plot **one** weather parameter, as there is only one axis available. Plotting multiple will clutter your graph significantly.

## Running the model

### Arguments
All available arguments can be listed by executing the following command: `pipenv run python main.py --help` from the root directory project.

### Executing the model
The model can be executed by running the command `pipenv run python main.py [all arguments]`, where `[all arguments]` stands for the arguments required to run the model. An example execution command for PowerShell is listed below.
```
pipenv run python main.py --start_ts 01-05-2019 --end_ts 31-08-2019 --step 30 --inversion_layer 500 --source_data ships.xlsx --measurements_data Geiranger_2015_2019_measurements.xlsx --station '[\"G\"]' --pm_type PM1 --weather_plot '[\"G_mxWS\"]'
```
