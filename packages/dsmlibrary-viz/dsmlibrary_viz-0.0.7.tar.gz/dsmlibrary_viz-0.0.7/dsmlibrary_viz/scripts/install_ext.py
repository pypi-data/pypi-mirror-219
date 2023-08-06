import os
import duckdb

def install_ext():
    duckdb.sql("install 'httpfs';")
    print("Installed duckdb httpfs done!")