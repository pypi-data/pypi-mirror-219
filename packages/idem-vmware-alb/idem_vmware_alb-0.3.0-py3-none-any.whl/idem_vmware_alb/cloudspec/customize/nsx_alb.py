import copy

from dict_tools.data import NamespaceDict


def run(hub, ctx):
    # This customization is used to create an additional folder "alb" to have a 5 segment function reference call
    updated_cloud_spec: NamespaceDict = copy.deepcopy(ctx.cloud_spec)
    for name, plugin in ctx.cloud_spec.get("plugins").items():
        new_plugin = updated_cloud_spec.get("plugins").pop(name)
        new_resource_name = "alb." + name
        for func_name, func_data in new_plugin.get("functions").items():
            func_data.get("hardcoded", {})["resource_name"] = new_resource_name
        updated_cloud_spec["plugins"][new_resource_name] = new_plugin

    ctx.cloud_spec = updated_cloud_spec
