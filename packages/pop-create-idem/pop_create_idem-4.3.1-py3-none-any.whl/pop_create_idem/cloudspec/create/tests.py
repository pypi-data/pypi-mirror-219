import os
import pathlib

from cloudspec import CloudSpec
from cloudspec import CloudSpecParam


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)

    for ref, plugin in cloud_spec.plugins.items():
        plugin["imports"] = ["import pytest"]

        for test_type in ["exec", "states", "tool"]:
            test_dir = (
                root_directory
                / "tests"
                / "integration"
                # test_module_type = exec, states, tool
                / test_type
            )

            template_dir = (
                root_directory
                / ctx.clean_name
                / "autogen"
                / ctx.service_name
                / "templates"
                / "tests"
                # test_module_type = exec, states, tool
                / test_type
            )

            mod_file = hub.cloudspec.parse.plugin.touch(
                root=test_dir, ref=ref, is_test=True
            )

            plugin["file_vars"] = {}
            if test_type == "states":
                # The states test should be run with --test and actual run mode
                plugin["file_vars"]["PARAMETRIZE"] = {
                    "argnames": "__test",
                    "argvalues": [True, False],
                    "ids": ["--test", "run"],
                }

            if test_type in ["states", "exec"]:
                # Add default global parameter for tracking a resource being created inside test
                # This helps in clean up of a created resource in test
                plugin["file_vars"]["PARAMETER"] = {
                    "name": "idem-test-resource- + TODO: Add unique identifier generator",
                }

            to_write = hub.cloudspec.parse.plugin.header(plugin)

            # Collect get_call_params beforehand from the list
            # This is helpful when a test method wants to call into GET after any operation in a test
            get_call_params = None
            test_get_func = [
                value for key, value in plugin.functions.items() if key == "test_get"
            ]
            if test_get_func:
                get_call_params = {
                    name: CloudSpecParam(name=name, **param_spec)
                    for name, param_spec in test_get_func[0]
                    .get("hardcoded", {})
                    .get("method_call_params", {})
                    .items()
                }

            for function_name, function_data in plugin.functions.items():
                if not function_name.startswith("test_"):
                    # Only process test functions
                    continue

                if test_type != function_data.hardcoded.test_module_type:
                    # Let's not add to the file if it doesn't belong to the module
                    continue

                request_format_template_file = f"{template_dir}/{function_name}.jinja2"
                default_request_format_template_file = f"{template_dir}/default.jinja2"
                if os.path.isfile(request_format_template_file):
                    with open(f"{template_dir}/{function_name}.jinja2", "rb+") as f:
                        request_format = f.read().decode()
                elif os.path.isfile(default_request_format_template_file):
                    with open(default_request_format_template_file, "rb+") as f:
                        request_format = f.read().decode()
                else:
                    request_format = cloud_spec.request_format.get(function_name)

                template = hub.tool.jinja.template(
                    f"{hub.cloudspec.template.test.TEST_FUNCTION}\n    {request_format}\n\n\n"
                )

                # Get call params for method's (being called in the test)
                method_call_params = {
                    name: CloudSpecParam(name=name, **param_spec)
                    for name, param_spec in function_data.hardcoded.method_call_params.items()
                }

                try:
                    method_call_name = function_data.hardcoded.method_call_name
                    to_write += template.render(
                        function={
                            "name": function_name,
                            "service_name": cloud_spec.service_name,
                            "hardcoded": {
                                "parametrize": True
                                if method_call_name in ["present", "absent"]
                                else False,
                                **function_data.hardcoded,
                            },
                            "method_call_name": method_call_name,
                            "method_call_params": hub.cloudspec.parse.param.all_call_params(
                                method_call_params
                            ),
                            "get_call_params": hub.cloudspec.parse.param.all_call_params(
                                get_call_params
                            )
                            if get_call_params is not None
                            else "",
                        },
                    )
                except Exception as err:
                    hub.log.warning(
                        f"Warning when generating function's action definitions for {function_name}: {err.__class__.__name__}: {err}"
                    )
            mod_file.write_text(to_write)
