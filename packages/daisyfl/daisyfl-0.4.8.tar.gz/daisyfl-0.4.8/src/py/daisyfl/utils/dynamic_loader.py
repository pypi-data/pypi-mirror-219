def dynamic_load(m, obj):
    module = __import__(m, fromlist=["import from sub-module"])
    return getattr(module, obj)