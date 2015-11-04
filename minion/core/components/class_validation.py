def is_nervous_system(obj):
    return hasattr(obj, 'publish') and hasattr(obj, 'listen')
