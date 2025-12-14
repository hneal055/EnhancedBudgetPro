import importlib

def test_import_ui_app():
 mod = importlib.import_module('ui_app')
 assert mod is not None
