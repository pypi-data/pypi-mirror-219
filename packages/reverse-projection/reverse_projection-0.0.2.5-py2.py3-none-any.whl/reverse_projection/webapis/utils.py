from flask import request
import sys
from pathlib import Path

def get_feature_ind(length: int, number_ind: int, target_ind: list, omit_ind: list=[]) -> list:
    feature_ind = []
    omit_ind_ = omit_ind + target_ind + [number_ind]
    for ind in range(length):
        if ind not in omit_ind_:
            feature_ind.append(ind)
    return feature_ind

def get_json(key: str):
    data = request.get_json().get(key)
    if key == "number_ind":
        data = int(data)
    elif key == "target_ind":
        data = [int(i) for i in data]
    return data

def get_file(key: str):
    return request.files.get(key)

def get_form(key: str):
    return request.form.get(key)

def html_template():
    return sys._getframe(1).f_code.co_name+".html"

def output_error(e):
    return f"{e}, {Path(e.__traceback__.tb_frame.f_globals['__file__']).stem}, {e.__traceback__.tb_lineno}"