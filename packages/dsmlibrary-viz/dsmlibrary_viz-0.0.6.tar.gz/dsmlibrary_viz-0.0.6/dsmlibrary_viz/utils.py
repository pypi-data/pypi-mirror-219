
def check_http_status_code(response, msg=""):
    if response.status_code >= 300:
        txt = response.json() if response.status_code < 500 else " "
        raise Exception(f"Some thing wrong {msg} {response.status_code}, {txt}")

def check_type(variable, variableName, dtype, child=None):
    if type(variable) != dtype:
        raise Exception(f"Expect {variableName} type {dtype} but got {type(variable)}")
    if child is not None:
        for elm in variable:
            if type(elm) != child:
                raise Exception(f"{variableName} expect [{child}, {child}, ... {child}] but has {elm}({type(elm)})")