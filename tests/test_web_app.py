import importlib

def test_import_web_app():
 mod = importlib.import_module('web_app')
 assert mod is not None
