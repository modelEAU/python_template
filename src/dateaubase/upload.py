import argparse
import os
from datetime import datetime as dt
from pathlib import Path, PurePath

import sqlalchemy
import yaml

import config
import datEAUbase as db
from data_file import DataCombiner, DataFile, get_file_reader
from tables import ValueTable

# Define global constants
TEST_CONFIG_RELATIVE_PATH = Path("../../config_file_upload_test.yaml")


def commit_to_dateaubase(values: ValueTable, engine: sqlalchemy.engine, db_name: str, variable: str, metadata_id: int):
    # Get current value for last value of the specific meta_ID
    last_timestamp_before = db.get_last_timestamp_for_variable(engine, metadata_id)
    # Import into datEAUbase
    db.send_to_db(values, engine)
    print(f"Added {len(values)} rows to {db_name}")

    # Get updated value for last value of the specific meta_ID
    last_timestamp_after = db.get_last_timestamp_for_variable(engine, metadata_id)
    print(f'{dt.fromtimestamp(last_timestamp_before)} - last RODTOX {variable} measurement in datEAUbase before import')
    print(f'{dt.fromtimestamp(last_timestamp_after)} - last RODTOX {variable} measurement in datEAUbase after import')


def connect_to_dateaubase(use_local: bool, conf: config.DatabaseConfig) -> sqlalchemy.engine:
    if use_local:
        engine = db.connect_local(str(conf.local_url), conf.database_name)
    else:
        engine = db.connect_remote(str(conf.remote_url), conf.database_name, str(conf.credentials_path))

    if not db.engine_runs(engine):
        raise ConnectionError(f"Could not connect to {conf.database_name}")
    return engine


def get_new_values_for_variable(
        variable_settings: config.Variable,
        engine: sqlalchemy.engine,
        file_structure: config.FileStructure,
        file_reader_class: DataFile) -> ValueTable:

    metadata_id = variable_settings.metadata_id

    path = PurePath(variable_settings.directory_path)

    last_id_for_table = db.get_last_value_id(engine)
    last_timestamp_for_var = db.get_last_timestamp_for_variable(engine, metadata_id)
    last_date_for_var = dt.fromtimestamp(last_timestamp_for_var)

    filepaths = [str(path.joinpath(x)) for x in os.listdir(str(path))]

    file_objects = [file_reader_class(
        filepath=filepath,
        file_structure=file_structure,
        variable=variable_settings) for filepath in filepaths]

    combiner = DataCombiner(last_id=last_id_for_table, last_date=last_date_for_var)
    for file in file_objects:
        combiner.add_file(file)

    return combiner.values


def main(settings: config.Config, use_local: bool) -> None:
    """Main import routine. It has the following main steps:
        1. Connect to the dateaubase
        2. Cycle through each file types defined in the config
        3. Cycle through each variable to import
        4. Collect all the new data in the files present in the directory defined in the config.
        5. Send the new data to the dateaubase, if any.

    Arguments:
        settings -- Config object with the database connection info,
                    the file structure information, and the variables
                    to import.
        use_local -- should be True on the dateaubase server, and False
                    when run from anywhere else.
    """
    print(dt.now())
    db_conf = settings.database_config
    engine = connect_to_dateaubase(use_local, db_conf)

    for file_config in settings.file_configs:
        file_structure = file_config.file_structure
        file_reader_class = get_file_reader(file_config.name)
        for variable in file_config.variables:

            data = get_new_values_for_variable(variable, engine, file_structure, file_reader_class)

            if data.empty:
                print(f"There are no new {variable.name} values to send to {db_conf.database_name}")
                continue

            commit_to_dateaubase(data, engine, db_conf.database_name, variable.name, variable.metadata_id)


def str_to_bool(s: str) -> bool:
    """Helper function to parse boolean flags received from the commead line"""
    if s.lower() in {'y', 'yes', 'true'}:
        return True
    if s.lower() in {'n', 'no', 'false'}:
        return False
    raise ValueError(f"Argument value {s} is neither 'true' or 'false'")


def read_config_from_file(path: str) -> config.Config:
    """Loads the configuration settings into a Config object from a yaml file"""
    pathObj = Path(path)
    if not pathObj.is_file():
        raise ValueError(f"Could not find config file at {path}")
    with open(pathObj) as f:
        file_config = yaml.safe_load(f)
    return config.Config(**file_config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import data from sensor files into datEAUbase')
    parser.add_argument('--config', type=str, default=TEST_CONFIG_RELATIVE_PATH, help='Location of the configuration file with the parsing instructions.')
    parser.add_argument('--local', type=str_to_bool, default=True)
    args = parser.parse_args()

    configuration = read_config_from_file(args.config)

    main(configuration, args.local)
