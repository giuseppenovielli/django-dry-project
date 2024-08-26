import inspect


def get_base_classes(instance):
    # https://stackoverflow.com/questions/1401661/list-all-base-classes-in-a-hierarchy-of-given-class
    class_type = type(instance)
    return list(inspect.getmro(class_type))