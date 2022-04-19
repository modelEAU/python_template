from typing import List

from pydantic import BaseModel


class Variable(BaseModel):
    directory_path: str
    name: str
    variable_name: str
    metadata_id: int
    scaling_factor: float


class FileStructure(BaseModel):
    separator: str
    encoding: str
    dt_format: str
    time_column: str
    timezone: str
    value_column: str
    variable_column: str
    validity_column: str
    validity_flag: int
    first_valid_row_idx: int
    last_valid_row_idx: int
    header_row_idx: int


class FileType(BaseModel):
    name: str
    file_structure: FileStructure
    variables: List[Variable]


class DatabaseConfig(BaseModel):
    database_name: str
    credentials_path: str
    local_url: str
    remote_url: str


class Config(BaseModel):
    file_configs: List[FileType]
    database_config: DatabaseConfig
