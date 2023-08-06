import json


import flywheel
from . import utils


class Filter:
    """
    Simple wrapper for a matching filter that can be applied to a context.

    Args:
        fields(dict): The field to value(s) mapping.
    """

    def __init__(self, fields):
        self.fields = fields

    def test(self, context):
        """
        Test context to see if it passes this filter. Top-level clauses (properties) are
        logically ANDed, and lists of values are logically ORed.

        Args:
            context (dict): The context to check

        Returns:
            bool: True if every top level clause matched
        """
        for prop, filter_value in self.fields.items():
            prop_val = utils.dict_lookup(context, prop)
            if isinstance(filter_value, list):
                if prop_val not in filter_value:
                    return False
            else:
                if prop_val != filter_value:
                    return False
        return True


class Resolver:
    """
    Compiled resolver rule

    Args:
        namespace (str): The template namespace
        resolverDef (dict): The resolver properties dictionary

    Attributes:
        namespace: The template namespace
        id: The optional resolver id
        templates: The list of template names (keys in definitions dict) this resolver applies to
        update_field: The field to be updated with the resolved result
        filter_field: The field that contains the user-defined filter
        container_type: The type of container this resolver should match
        resolve_for: The level that resolution for this resolver should take place (e.g. session)
        format: The format string for resolved values
        value: The path to the value to copy, if not using a format string
    """

    def __init__(self, namespace, resolverDef, fw, save_sidecar_as_metadata=False):
        self.namespace = namespace
        self.id = resolverDef.get("id")
        self.templates = resolverDef.get("templates", [])
        self.update_field = resolverDef.get("update")
        self.filter_field = resolverDef.get("filter")
        self.container_type = resolverDef.get("type")
        self.resolve_for = resolverDef.get("resolveFor")
        self.format = resolverDef.get("format")
        self.value = resolverDef.get("value")
        self.save_sidecar_as_metadata = save_sidecar_as_metadata
        self.client = fw

        if self.format and self.value:
            print(
                'WARNING: Because "format" is specified, "value" will be ignored for resolver: {}'.format(
                    self.id
                )
            )

    def resolve(self, context):
        """
        Resolve update_field for context by matching and formatting children of session.

        Args:
            context (dict): The context to update
        """
        results = []

        parent = context.get(self.resolve_for)
        if not parent:
            return

        # Determine filter fields, and add namespace prefix for matching
        filter_fields = utils.dict_lookup(context, self.filter_field, {})
        base_fields = {}
        if self.container_type:
            base_fields["container_type"] = self.container_type

        filters = []
        for entry in filter_fields:
            fields = base_fields.copy()
            for k, v in entry.items():
                key = "{}.info.{}.{}".format(self.container_type, self.namespace, k)
                fields[key] = v
            filters.append(Filter(fields))

        # Iterate through the contexts in the session, collecting matches
        for ctx in parent.context_iter():
            for filt in filters:
                if filt.test(ctx):
                    if self.format:
                        results.append(utils.process_string_template(self.format, ctx))
                    elif self.value:
                        value = utils.dict_lookup(ctx, self.value, None)
                        if value:
                            if results and results != value:
                                print(
                                    "WARNING: multiple different matches when resolving results, will take last match!"
                                )
                            results = value

        # Finally update the field specified
        if self.save_sidecar_as_metadata:  # then update that metadata
            utils.dict_set(context, self.update_field, results)
        else:  # using actual sidecar, not metadata, so update that json file
            # get name of side car
            nifti_name = context["file"].data["name"]
            if not nifti_name.endswith(".nii.gz"):
                print(
                    f"Unexpected file name '{nifti_name}', should end with '.nii.gz'  "
                )
            else:
                sidecar_name = nifti_name[:-7] + ".json"
                acquisition = self.client.get_acquisition(
                    context["acquisition"].data["id"]
                )
                sidecar_contents = acquisition.read_file(sidecar_name)
                if not sidecar_contents:
                    print(f"Unable to load {sidecar_name}")
                sidecar_json = json.loads(sidecar_contents)
                field_name = self.update_field.split(".")[-1]
                sidecar_json[field_name] = results
                json_str = json.dumps(sidecar_json, indent=4)
                file_spec = flywheel.FileSpec(sidecar_name, json_str, "text/plain")
                acquisition.upload_file(file_spec)
