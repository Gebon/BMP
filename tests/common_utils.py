import os


def get_path_to_resource(resource_name):
    script_path = os.path.dirname(os.path.realpath(__file__))
    join = os.path.join
    test_res_path = join(script_path, "test_res")

    return join(test_res_path, resource_name)
