# pandas_options.py

import os

import pandas as pd  # noqa: F401


# Usage:
# Import this configuration file at the beginning of your script
# Example:
# > from service.pandas_options import PandasConfig
# > PandasConfig.apply_settings()


class PandasConfig:
    @staticmethod
    def apply_settings():
        # clear console
        os.system("cls")

        # Set display options for pandas globally
        # ---------------------------
        # Show all columns in the output
        pd.set_option("display.max_columns", None)
        # Show up to 100 rows in the output (set to None for unlimited)
        pd.set_option("display.max_rows", 250)
        # Increase the line width limit to 1000 characters (adjust as needed)
        pd.set_option("display.width", 1000)

        # Other available configurations:
        # ------------------------------
        # pd.set_option('display.max_rows', None)  # Show all rows
        # pd.set_option('display.max_columns', 20)  # Set a limit for columns to display
        pd.set_option("display.float_format", "{:.2f}".format)  # Format floats to 2 decimal places
        # pd.set_option('display.colheader_justify', 'right')  # Align column headers to the right
        # pd.set_option('display.max_colwidth', 50)  # Set maximum width of each column
