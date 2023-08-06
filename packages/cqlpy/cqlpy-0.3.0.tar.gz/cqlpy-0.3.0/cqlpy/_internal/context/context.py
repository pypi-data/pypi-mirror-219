import json
from typing import Optional, Union
from cqlpy._internal.context.cql_valueset_provider import CqlValuesetProvider

from cqlpy._internal.context.fhir.r4.model import FhirR4DataModel
from cqlpy._internal.context.parameter_provider import ParameterProvider
from cqlpy._internal.parameter import Parameter
from cqlpy._internal.types.code import Code
from cqlpy._internal.types.valueset import Valueset
from cqlpy._internal.types.valueset_scope import ValuesetScope
from cqlpy._internal.providers.valueset_provider import ValuesetProvider

from cqlpy._internal.exceptions import CqlPyValueError


class Context:
    """
    A context is a required parameter on every CQL expression that is converted to python as a function.

    ## Usage

    The expected signature of every function that implements a CQL Expression is:

    ```python
    def EXPRESSION_NAME(context: Context):
    ```

    The Context provides access to the data model, parameter values, and value set codes as needed by the internal elements
    of a python function that implements a CQL expression. The Context provides access to these concepts via a retrieve operation
    that is implemented with syntax such as:

    ```python
    context["Encounter"]    # if a string is requested (assumed to be a FHIR resource type), context returns a
                            # list of Resources from the model, in this case all Encounter resources.

    context["Encounter", Valueset, "type"]
                            # if a tuple is requested (assumed to be a FHIR resource type), context returns a
                            # list of Resources from the model, in this case Encounter resources, filtered by
                            # checking the specified property to see if it has a coded value in the specified value set.

    context[Parameter]      # if a Parameter is requested, context returns the type specified by the Parameter
                            # with value determined by the parameter_provider from external parameters or the default value.

    context[Valueset]       # if a Valueset is requested, context returns a Valueset that includes with Codes property populated
                            # from the valueset_provider.
    ```

    The Context iterates through the bundle (as a json object) to retrieve a list of Resources.

    Properties of Resources can be obtained using syntax such as:

    ```
    Encounter["period"]     # The property of the resource is properly typed when requested (in this case, Interval)
                            # by parsing the related bundle json element.
    ```

    Context Resource retrieve operations and Resource property retrieve operations are cached so that iterating through the bundle
    and parsing json is only performed once (at time of the first request).
    """

    def __init__(
        self,
        valueset_provider: ValuesetProvider,
        bundle: Optional[Union[str, dict]] = None,
        bundle_file_name: Optional[str] = None,
        parameters: Optional[dict] = None,
    ):
        """
        Create a new Context.

        ## Parameters

        - `valueset_provider`: A `cqlpy.providers.ValuesetProvider` that is used to retrieve valuesets by id.
            Available providers are in `cqlpy.providers`.
        - `bundle`: A json object that represents a FHIR bundle.
        - `bundle_file_name`: A file name that contains a FHIR bundle as JSON.
        - `parameters`: Parameters used to control execution of the CQL.
        """

        parsed_bundle = None
        if bundle_file_name:
            with open(bundle_file_name, encoding="utf-8") as f:
                parsed_bundle = json.loads(f.read())

        if isinstance(bundle, str):
            parsed_bundle = json.loads(bundle)

        if isinstance(bundle, dict):
            parsed_bundle = bundle

        if parsed_bundle is None:
            raise CqlPyValueError("bundle or bundle_file_name must be specified")

        self.parameter_provider = ParameterProvider(parameters)
        self.model = FhirR4DataModel(parsed_bundle, self.parameter_provider)
        self.cql_valueset_provider = CqlValuesetProvider(
            valueset_provider=valueset_provider
        )

    def __getitem__(
        self,
        requested_concept: Union[
            Parameter,
            Valueset,
            ValuesetScope,
            str,
            tuple[str, Union[Valueset, list[Code], Code], str],
        ],
    ):
        if isinstance(requested_concept, Parameter):
            # In this case, the return type will be the Cql Type specified by the parameter,
            # i.e. Interval<DateTime>, CqlString, etc.
            return self.parameter_provider[requested_concept]

        if isinstance(requested_concept, Valueset) or isinstance(
            requested_concept, ValuesetScope
        ):
            # In this case, the return type will be ValueSet (which includes all codes specified by the value set).
            return self.cql_valueset_provider[requested_concept]

        if isinstance(requested_concept, Code):
            # In this case, there is nothing to lookup... the Code is fully populated.
            return requested_concept

        return self.model[requested_concept]
