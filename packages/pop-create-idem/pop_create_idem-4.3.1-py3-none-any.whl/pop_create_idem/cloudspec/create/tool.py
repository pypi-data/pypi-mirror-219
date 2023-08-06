import os
import pathlib

import tqdm

from cloudspec import CloudSpec


def run(hub, ctx, root_directory: pathlib.Path):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = CloudSpec(**ctx.cloud_spec)
    tool_dir = root_directory / ctx.clean_name / "tool" / ctx.service_name
    template_dir = (
        root_directory
        / ctx.clean_name
        / "autogen"
        / ctx.service_name
        / "templates"
        / "tool"
    )

    for ref, plugin in cloud_spec.plugins.items():
        mod_file = hub.cloudspec.parse.plugin.touch(tool_dir, ref)
        ref = hub.cloudspec.parse.plugin.ref(ctx, ref)
        module_ref = hub.cloudspec.parse.plugin.mod_ref(ctx, ref, plugin)

        # Set up the base template
        if not plugin.functions:
            to_write = hub.cloudspec.parse.plugin.header(plugin)
        else:
            to_write = hub.cloudspec.parse.plugin.header(plugin)
            for func_name, func_data in tqdm.tqdm(
                plugin.functions.items(), desc=f"{ref} tool functions"
            ):
                if func_name in [
                    "get",
                    "list",
                    "create",
                    "update",
                    "delete",
                    "present",
                    "absent",
                    "describe",
                ] or func_name.startswith("test_"):
                    # These functions are not for tool module
                    continue

                function_request_format_template_file = (
                    f"{template_dir}/{func_name}.jinja2"
                )
                default_request_format_template_file = f"{template_dir}/default.jinja2"
                if os.path.isfile(function_request_format_template_file):
                    with open(function_request_format_template_file, "rb+") as f:
                        request_format = f.read().decode()
                elif os.path.isfile(default_request_format_template_file):
                    with open(default_request_format_template_file, "rb+") as f:
                        request_format = f.read().decode()
                else:
                    # cloudspec was provided with hardcoded request format
                    request_format = cloud_spec.request_format.get(func_name)

                template = hub.tool.jinja.template(
                    f"{hub.cloudspec.template.tool.FUNCTION}\n    {request_format}\n\n"
                )

                try:
                    to_write += template.render(
                        function=dict(
                            name=func_name,
                            ref=ref,
                            module_ref=f"tool.{module_ref}",
                            **func_data,
                            header_params=hub.cloudspec.parse.param.headers(
                                func_data.params
                            ),
                        ),
                        parameter=dict(
                            mapping=hub.cloudspec.parse.param.mappings(func_data.params)
                        ),
                    )
                except Exception as err:
                    hub.log.warning(
                        f"Warning when generating function's action definitions for {func_name}: {err.__class__.__name__}: {err}"
                    )

        mod_file.write_text(to_write)
