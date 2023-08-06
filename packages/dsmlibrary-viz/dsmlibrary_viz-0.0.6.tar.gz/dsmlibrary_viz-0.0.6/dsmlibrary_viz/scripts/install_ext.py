import os
import duckdb

def install_ext():
    duckdb.sql("install 'httpfs';")
    os.system("echo 'Installed duckdb httpfs done!'")