import csv
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import datetime as dt
from typing import Any, List

import numpy as np
import pandas as pd

import tables
from config import FileStructure, Variable


class MissingFileTypeError(Exception):
    pass


@dataclass
class DataFile(ABC):
    filepath: str
    file_structure: FileStructure
    variable: Variable

    @abstractproperty
    def raw_data(self) -> pd.DataFrame:
        """Returns the data found in the file as a DataFrame"""

    @abstractmethod
    def get_first_date(self) -> pd.Timestamp:
        """Returns the date of the first value in the file."""

    @abstractmethod
    def get_last_date(self) -> pd.Timestamp:
        """Returns the date of the last value in the file."""

    @abstractproperty
    def values(self) -> tables.ValueTable:
        """Returns the values present in the file as a ValueTable"""


class TextDBFile(DataFile):
    def find_time_col_pos(self, header_row: List[Any], time_col_name: str) -> int:
        return header_row.index(time_col_name)

    def get_timestamp_from_row(self, filename: str, structure: FileStructure, row_index: int):
        with open(filename, "r", encoding=structure.encoding) as f:
            rows = list(csv.reader(f, delimiter=structure.separator))
        time_col_pos = self.find_time_col_pos(rows[structure.header_row_idx], structure.time_column)
        return pd.to_datetime(rows[row_index][time_col_pos], format=structure.dt_format)

    @property
    def raw_data(self) -> pd.DataFrame:
        return pd.read_csv(
            self.filepath,
            sep=self.file_structure.separator,
            encoding=self.file_structure.encoding,
            on_bad_lines='skip',
            header=self.file_structure.header_row_idx)

    def get_first_date(self) -> pd.Timestamp:
        return self.get_timestamp_from_row(self.filepath, self.file_structure, self.file_structure.first_valid_row_idx)

    def get_last_date(self) -> pd.Timestamp:
        return self.get_timestamp_from_row(self.filepath, self.file_structure, self.file_structure.last_valid_row_idx)


class RodtoxFile(TextDBFile):

    @property
    def values(self) -> tables.ValueTable:
        df = self.raw_data.copy()
        structure = self.file_structure
        variable = self.variable
        # Remove invalid entries from the data
        df = df.loc[df[structure.validity_column] == 1]
        # Only keep rows where the probe sends a DO measurement
        df = df.loc[df[structure.variable_column] == variable.name]
        # Replace commas by dots so that values are treated as floats instead of strings
        df[structure.value_column].replace({',': '.'}, regex=True, inplace=True)
        # Transform the values from strings into numbers
        df[structure.value_column] = pd.to_numeric(df[structure.value_column])

        # Transform the timestamps into machine-readable DateTime objects
        df[structure.time_column] = pd.to_datetime(df[structure.time_column], format=structure.dt_format, utc=False)
        df[structure.time_column] = df[structure.time_column].dt.tz_localize(structure.timezone).astype(np.int64) // 1e9

        # Transform raw data table into valid ValueTable
        df['Metadata_ID'] = variable.metadata_id
        df["Number_of_experiment"] = 1
        df["Comment_ID"] = np.nan

        df.reset_index(inplace=True)
        df = df.rename(columns={
            'index': 'Value_ID',
            structure.time_column: "Timestamp",
            structure.value_column: "Value",
        })
        df = df[[col for col in df.columns if col in tables.ValueTable.acceptable_columns]]
        return tables.ValueTable(df)


class AnaproFile(TextDBFile):
    @property
    def values(self) -> tables.ValueTable:
        df = self.raw_data.copy()
        structure = self.file_structure
        variable = self.variable
        clean_names = {col: col.split("]")[0] for col in df.columns}
        for old, new in clean_names.items():
            if "[" in new:
                clean_names[old] = new + "]"
            if "Temp. " in new:
                clean_names[old] = 'Temp.'

        df.rename(columns=clean_names, inplace=True)
        df.fillna(0, inplace=True)
        # Transform the timestamps into machine-readable DateTime objects
        df[structure.time_column] = pd.to_datetime(df[structure.time_column], format=structure.dt_format, utc=False)
        df[structure.time_column] = df[structure.time_column].dt.tz_localize(structure.timezone).astype(np.int64) // 1e9

        # Transform raw data table into valid ValueTable
        df['Metadata_ID'] = variable.metadata_id
        df["Number_of_experiment"] = 1
        df["Comment_ID"] = np.nan

        df.reset_index(inplace=True)
        df = df.rename(columns={
            'index': 'Value_ID',
            structure.time_column: "Timestamp",
            variable.variable_name: "Value",
        })
        df["Value"] = df["Value"] * variable.scaling_factor
        df = df[[col for col in df.columns if col in tables.ValueTable.acceptable_columns]]
        return tables.ValueTable(df)


class DataCombiner:
    def __init__(self, last_id: int, last_date: dt) -> None:
        self.last_db_date = last_date
        self.last_db_id = last_id
        self.files: List[DataFile] = []

    @property
    def values(self) -> tables.ValueTable:
        if not self.files:
            df = None
        else:
            dfs = [file.values for file in self.files]
            df = pd.concat(dfs, axis=0)
            df = df.reset_index(drop=True)
            df.sort_values("Timestamp", inplace=True)
            df = df.loc[df["Timestamp"] > self.last_db_date.timestamp()]
            df['Value_ID'] = df.index + self.last_db_id + 1
        return tables.ValueTable(df)

    def add_file(self, file: DataFile) -> None:
        if file.get_last_date() < self.last_db_date:
            return
        self.files.append(file)

    @property
    def first_date(self) -> pd.Timestamp:
        return min(file.get_first_date() for file in self.files)

    @property
    def last_date(self) -> pd.Timestamp:
        return max(file.get_last_date() for file in self.files)


def get_file_reader(file_type: str) -> DataFile:
    if file_type in {'rodtox'}:
        return RodtoxFile
    if file_type in {'anapro'}:
        return AnaproFile
    raise MissingFileTypeError(f"{file_type} has no defined DataFile class.")
