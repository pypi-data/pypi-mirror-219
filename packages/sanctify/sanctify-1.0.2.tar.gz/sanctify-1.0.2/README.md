# Sanctify

Sanctify is a Python package designed to facilitate data cleansing and validation operations on pandas DataFrames. It provides a set of predefined transformations and validations that can be applied to different columns of a DataFrame based on a column mapping schema. The package allows you to define data types, transformations, and validations for each column, making it easy to clean and validate your data.

## Features

- Cleansing and validation of data in pandas DataFrames.
- Support for custom transformations and validations.
- Configurable column mapping schema to define data types and operations for each column.
- Built-in transformations for common data cleaning tasks.
- Validation functions for common data validation checks.
- Flexibility to handle various data types and formats.
- Ability to handle missing or malformed data gracefully.

## Installation

You can install Sanctify using pip:

```shell
pip install sanctify
```

## Usage
```python
from enum import StrEnum, auto
from time import perf_counter

import pandas as pd
from frozendict import frozendict
from loguru import logger

from sanctify.cleanser import Cleanser
from sanctify.constants import (
    ComparisonOperations,
    Constants,
    DateOrderTuples,
)
from sanctify.processor import process_cleansed_df
from sanctify.transformer import Transformer
from sanctify.validator import Validator
from functools import wraps


class MyCustomDataTypes(StrEnum):
    """Enumeration for different data types in a csv."""

    ACCOUNT = auto()
    NAME = auto()
    DOB = auto()
    PHONE = auto()
    ZIP_CODE = auto()
    AMOUNT = auto()
    TEXT = auto()
    DECIMAL = auto()
    SSN = auto()
    STATE = auto()
    DATE = auto()


class MyMandatoryColumns(StrEnum):
    """Enumeration for mandatory columns in a csv."""

    ACCOUNT_NUMBER = "Account"
    STATE = "State"
    CALLER_NUMBER = "Phone"
    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    ZIP_CODE = "Zip Code"
    DATE_OF_BIRTH = "DOB"
    LATEST_DUE_DATE = "Latest Due Date"
    LATEST_DUE_AMOUNT = "Latest Due Amount"
    SSN = "SSN"


class CountryCodes(StrEnum):
    """Enumeration for country codes."""

    INDIA = "91"
    US = "1"


# Dictionary representing column mapping schema
COLUMN_MAPPING_SCHEMA = frozendict(
    {
        "First Name": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.FIRST_NAME.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.NAME.value,
        },
        "Last Name": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.LAST_NAME.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.NAME.value,
        },
        "DOB": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.DATE_OF_BIRTH.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.DOB,
        },
        "Cell Phone": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.CALLER_NUMBER.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.PHONE,
        },
        "Zip": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.ZIP_CODE.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.ZIP_CODE.value,
        },
        "State": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.STATE.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.STATE.value,
        },
        "SSN#": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.SSN.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.SSN.value,
        },
        "Account Due Date": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.LATEST_DUE_DATE.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.DATE.value,
        },
        "Due Amount": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.LATEST_DUE_AMOUNT.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.AMOUNT.value,
        },
        "Customer Number": {
            Constants.STANDARD_COLUMN.value: MyMandatoryColumns.ACCOUNT_NUMBER.value,
            Constants.DATA_TYPE.value: MyCustomDataTypes.ACCOUNT.value,
        },
    }
)


# Dictionary representing data type schema
DATA_TYPE_SCHEMA = frozendict(
    {
        MyCustomDataTypes.ACCOUNT.value: {
            Constants.TRANSFORMATIONS.value: [
                Transformer.remove_punctuations,
            ],
        },
        MyCustomDataTypes.NAME.value: {
            Constants.TRANSFORMATIONS.value: [
                Transformer.convert_to_lowercase,
                Transformer.replace_ii_with_II,
                Transformer.convert_jr_to_Junior,
                Transformer.convert_sr_to_Senior,
                Transformer.remove_dot_from_string,
            ],
        },
        MyCustomDataTypes.DOB.value: {
            Constants.TRANSFORMATIONS.value: [
                (
                    Transformer.parse_date_from_string,
                    {
                        Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value
                    },
                )
            ],
            Constants.VALIDATIONS.value: [
                (
                    Validator.validate_age,
                    {
                        Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value,
                        Constants.COMPARISON_OPERATIONS.value: {
                            ComparisonOperations.GREATER_THAN_EQUALS.value: 18,
                            ComparisonOperations.LESS_THAN_EQUALS.value: 100,
                        },
                    },
                )
            ],
        },
        MyCustomDataTypes.DATE.value: {
            Constants.TRANSFORMATIONS.value: [
                (
                    Transformer.parse_date_from_string,
                    {
                        Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value
                    },
                )
            ],
        },
        MyCustomDataTypes.PHONE.value: {
            Constants.TRANSFORMATIONS.value: [Transformer.extract_phone_number],
            Constants.POST_PROCESSING_DATA_TYPE.value: int,
        },
        MyCustomDataTypes.AMOUNT.value: {
            Constants.TRANSFORMATIONS.value: [
                Transformer.remove_currency_from_amount,
            ],
            Constants.POST_PROCESSING_DATA_TYPE.value: float,
        },
        MyCustomDataTypes.SSN.value: {
            Constants.TRANSFORMATIONS.value: [Transformer.remove_punctuations]
        },
        MyCustomDataTypes.ZIP_CODE.value: {
            Constants.VALIDATIONS.value: [Validator.validate_zip_code]
        },
        MyCustomDataTypes.STATE.value: {
            Constants.TRANSFORMATIONS.value: [Transformer.remove_punctuations]
        },
    }
)


def time_profiler(func):
    """Decorator to log total time taken by a function to execute."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        s = perf_counter()

        func_res = func(*args, **kwargs)

        t_seconds = perf_counter() - s
        logger.debug(f"TIME TAKEN TO {func.__name__} = {round(t_seconds, 3)} seconds\n")
        return func_res

    return wrapped


@time_profiler
def test_csv_parsing():
    """Function to test parsing operations."""
    input_file_path = "<path to>/input.csv"
    cleansed_output_file_path = (
        "<path to>/CLEANSED_input.csv"
    )
    processed_output_file_path = (
        "<path to>/PROCESSED_input.csv"
    )
    cleansed_processed_output_file_path = (
        "<path to>/CLEANSED_PROCESSED_input.csv"
    )

    input_df = pd.read_csv(input_file_path, dtype=str)
    cleanser = Cleanser(df=input_df, column_mapping_schema=COLUMN_MAPPING_SCHEMA)

    # Step 2: Read the CSV data

    # Step 3: Perform cleansing operations
    _ = cleanser.remove_trailing_spaces_from_column_headers()
    _ = cleanser.drop_unmapped_columns()
    _ = cleanser.drop_fully_empty_rows()
    _ = cleanser.remove_trailing_spaces_from_each_cell_value()
    _, updated_column_mapping_schema = cleanser.replace_column_headers()

    cleanser.df.to_csv(cleansed_output_file_path, index=False)

    processed_df = process_cleansed_df(
        df=cleanser.df,
        column_mapping_schema=updated_column_mapping_schema,
        data_type_schema=DATA_TYPE_SCHEMA,
    )

    processed_df.to_csv(processed_output_file_path, index=False)

    cleanser = Cleanser(df=processed_df, column_mapping_schema=COLUMN_MAPPING_SCHEMA)

    duplicates_marked_df = cleanser.mark_all_duplicates(
        columns=[
            MyMandatoryColumns.ACCOUNT_NUMBER.value,
            MyMandatoryColumns.CALLER_NUMBER.value,
        ],
    )

    cleanser = Cleanser(
        df=duplicates_marked_df, column_mapping_schema=COLUMN_MAPPING_SCHEMA
    )
    final_test_df = cleanser.drop_rows_with_errors(inplace=True)

    final_test_df.to_csv(cleansed_processed_output_file_path, index=False)


if __name__ == "__main__":
    test_csv_parsing()  # TIME TAKEN TO test_csv_parsing = x.yza seconds
```

## Contributing
Contributions to Sanctify are welcome! If you find any bugs, have feature requests, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/skit-ai/sanctify/).

## Code Coverage
[![codecov](https://codecov.io/gh/skit-ai/sanctify/branch/main/graph/badge.svg?token=WZHSY8T8SC)](https://codecov.io/gh/skit-ai/sanctify)
