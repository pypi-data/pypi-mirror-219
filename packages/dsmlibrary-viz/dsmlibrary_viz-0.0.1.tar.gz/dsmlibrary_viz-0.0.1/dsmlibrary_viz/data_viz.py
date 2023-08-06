import re
import duckdb
from . import base

class DataViz(base.Base):
    
    def __init__(self, token=None, verbose=True, dataplatform_api_uri=None, object_storage_uri=None, apikey=None):
        try:
            duckdb.sql("install 'httpfs';")
        except Exception as e:
            pass
        super().__init__(token, verbose, dataplatform_api_uri, object_storage_uri, apikey)

    def _find_fileID(self, match):
        match = match.group()
        _file_id = match.split(':')[-1]
        meta = self.get_meta_file(file_id=_file_id)
        return f"s3://dataplatform/{meta.get('s3_key')}/*.parquet"

    def _query(self, query_str):
        _storage_options = self._storage_options
        query = f"""
        load 'httpfs';
        SET s3_endpoint='{_storage_options.get('client_kwargs',{}).get('endpoint_url', "").replace("http://","")}';
        SET s3_access_key_id='{_storage_options.get('key', "PLEASE INPUT ACCESS KEY")}';
        SET s3_secret_access_key='{_storage_options.get('secret', "PLEASE INPUT SECRET KEY")}';
        SET s3_url_style = 'path';
        SET s3_use_ssl=false;
        {query_str}
        """
        query = re.sub("DISCOVERY:\d*", self._find_fileID, query)
        return query

    def query(self, query_str):
        query = self._query(query_str)
        return duckdb.sql(query).to_df()