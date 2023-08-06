import requests
import time
from . import utils

defind_clear_output = False
try:
    from IPython.display import clear_output
    defind_clear_output = True
except:
    pass

class Base:
    def __init__(
        self, token=None, verbose=True, 
        dataplatform_api_uri=None, object_storage_uri=None, 
        apikey=None
    ):
        
        self._verbose = verbose
        
        self._base_osd_url = object_storage_uri
            
        self._base_discovery_api = dataplatform_api_uri
        self._discovery_api = f"{dataplatform_api_uri}/api/v2"
        
        if (token is None) and (apikey is None):
            print("Please get token from discovery")
            token = input("Your Token : ")
            if defind_clear_output:
                time.sleep(2)
                clear_output()
        if (token in [None, '']) and apikey == None:
            raise Exception('Please enter your token from discovery')
        
        self._jwt_header = {
            'Authorization': f'Bearer {token}'
        }
        if apikey != None:
            self._jwt_header = {
                'Authorization': f'Api-Key {apikey}'
            }
            
        _res = requests.get(f"{self._discovery_api}/account/me/", headers=self._jwt_header)
        utils.check_http_status_code(response=_res, msg="Can not connect to DataPlatform")

        _res = requests.get(f"{self._base_discovery_api}/api/minio/minio-user/me/", headers=self._jwt_header)
        utils.check_http_status_code(response=_res, msg="Can not get objectstorage user")
        _data_osd = _res.json()
        
        self._storage_options = {
            'key': _data_osd.get('access', "-"),
            'secret': _data_osd.get('secret', "-"),
            'client_kwargs':{
                'endpoint_url': object_storage_uri
            },
            'use_listings_cache': False,
            'default_fill_cache': False,
        }
        if self._verbose: print("Init DataNode sucessful!")
        
    def get_meta_file(self, file_id):
        _res = requests.get(f'{self._discovery_api}/file/{file_id}/',  headers=self._jwt_header)
        utils.check_http_status_code(response=_res, msg=f'Cannot read meta data of file_id {file_id}')
        return _res.json()