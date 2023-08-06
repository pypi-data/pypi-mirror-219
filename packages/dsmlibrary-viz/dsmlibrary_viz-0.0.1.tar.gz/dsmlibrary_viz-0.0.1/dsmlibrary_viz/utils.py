
def check_http_status_code(response, msg=""):
    if response.status_code >= 300:
        txt = response.json() if response.status_code < 500 else " "
        raise Exception(f"Some thing wrong {msg} {response.status_code}, {txt}")