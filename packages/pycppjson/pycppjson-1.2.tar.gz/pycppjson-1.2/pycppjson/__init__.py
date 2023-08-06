from typing import Callable
from pycppjson.dumper import dump as _dump
from pycppjson.loader import load as _load

def load(JSONobj:str="{}", eval_:Callable=eval) -> dict:
	return eval_(_load(JSONobj))

def dump(PyOBJ:str | dict) -> str:
	if isinstance(PyOBJ, str):
		return _dump(PyOBJ)
	elif isinstance(PyOBJ, dict):
		return _dump(str(PyOBJ))
	else:
		raise NotImplemented