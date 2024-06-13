from dataclasses import dataclass, field

from .resource import Resource, ResourcePointer, ResourceSpec
from .role import Role
from .table import Table
from .view import View

# from .external_table import ExternalTable
# from .stage import Stage
from ..enums import ParseableEnum, ResourceType
from ..scope import SchemaScope
from ..props import BoolProp, FlagProp, IdentifierProp, Props, StringProp, TimeTravelProp


class StreamType(ParseableEnum):
    TABLE = "TABLE"
    EXTERNAL_TABLE = "EXTERNAL TABLE"
    STAGE = "STAGE"
    VIEW = "VIEW"


@dataclass(unsafe_hash=True)
class _TableStream(ResourceSpec):
    name: str
    on_table: Table
    owner: Role = "SYSADMIN"
    copy_grants: bool = None
    at: dict[str, str] = None
    before: dict[str, str] = None
    append_only: bool = None
    show_initial_rows: bool = field(default_factory=None, metadata={"triggers_replacement": True})
    comment: str = None

    def __post_init__(self):
        super().__post_init__()
        if self.at:
            self.at = {k.lower(): v for k, v in self.at.items()}
        if self.before:
            self.before = {k.lower(): v for k, v in self.before.items()}


class TableStream(Resource):
    """
    Description:
        Represents a stream on a table in Snowflake, which allows for change data capture on the table.
        This resource is used to create, replace, or check the existence of a stream on a specified table.

    Snowflake Docs:
        https://docs.snowflake.com/en/sql-reference/sql/create-stream.html

    Fields:
        name (string, required): The name of the stream.
        on_table (string, required): The name of the table the stream is based on.
        owner (string or Role): The role that owns the stream. Defaults to "SYSADMIN".
        copy_grants (bool): Whether to copy grants from the source table to the stream.
        at (dict): A dictionary specifying the point in time for the stream to start, using keys like TIMESTAMP, OFFSET, STATEMENT, or STREAM.
        before (dict): A dictionary specifying the point in time for the stream to start, similar to 'at' but defining a point before the specified time.
        append_only (bool): If set to True, the stream records only append operations.
        show_initial_rows (bool): If set to True, the stream includes the initial rows of the table at the time of stream creation.
        comment (string): An optional description for the stream.

    Python:

        ```python
        stream = TableStream(
            name="some_stream",
            on_table="some_table",
            owner="SYSADMIN",
            copy_grants=True,
            at={"TIMESTAMP": "2022-01-01 00:00:00"},
            before={"STREAM": "some_other_stream"},
            append_only=False,
            show_initial_rows=True,
            comment="This is a sample stream."
        )
        ```

    Yaml:

        ```yaml
        streams:
          - name: some_stream
            on_table: some_table
            owner: SYSADMIN
            copy_grants: true
            at:
              TIMESTAMP: "2022-01-01 00:00:00"
            before:
              STREAM: some_other_stream
            append_only: false
            show_initial_rows: true
            comment: This is a sample stream.
        ```
    """

    resource_type = ResourceType.STREAM
    props = Props(
        copy_grants=FlagProp("copy grants"),
        on_table=IdentifierProp("on table", eq=False),
        at=TimeTravelProp("at"),
        before=TimeTravelProp("before"),
        append_only=BoolProp("append_only"),
        show_initial_rows=BoolProp("show_initial_rows"),
        comment=StringProp("comment"),
    )
    scope = SchemaScope()
    spec = _TableStream

    def __init__(
        self,
        name: str,
        on_table: str,
        owner: str = "SYSADMIN",
        copy_grants: bool = None,
        at: dict[str, str] = None,
        before: dict[str, str] = None,
        append_only: bool = None,
        show_initial_rows: bool = None,
        comment: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._data = _TableStream(
            name=name,
            on_table=on_table,
            owner=owner,
            copy_grants=copy_grants,
            at=at,
            before=before,
            append_only=append_only,
            show_initial_rows=show_initial_rows,
            comment=comment,
        )
        self.requires(self._data.on_table)
        if self._data.at and "stream" in self._data.at:
            self.requires(ResourcePointer(name=self._data.at["stream"], resource_type=ResourceType.STREAM))
        if self._data.before and "stream" in self._data.before:
            self.requires(ResourcePointer(name=self._data.before["stream"], resource_type=ResourceType.STREAM))


# @dataclass(unsafe_hash=True)
# class _ExternalTableStream(ResourceSpec):
#     name: str
#     on_external_table: str
#     owner: str = "SYSADMIN"
#     copy_grants: bool = None
#     at: dict[str, str] = None
#     before: dict[str, str] = None
#     insert_only: bool = None
#     comment: str = None


# class ExternalTableStream(Resource):
#     """
#     CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
#       <name>
#       [ COPY GRANTS ]
#       ON EXTERNAL TABLE <external_table_name>
#       [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) ]
#       [ INSERT_ONLY = TRUE ]
#       [ COMMENT = '<string_literal>' ]
#     """

#     resource_type = ResourceType.STREAM
#     props = Props(
#         copy_grants=FlagProp("copy grants"),
#         on_external_table=IdentifierProp("on external table", eq=False),
#         at=TimeTravelProp("at"),
#         before=TimeTravelProp("before"),
#         insert_only=BoolProp("insert_only"),
#         comment=StringProp("comment"),
#     )
#     scope = SchemaScope()
#     spec = _ExternalTableStream

#     def __init__(
#         self,
#         name: str,
#         on_external_table: str,
#         owner: str = "SYSADMIN",
#         copy_grants: bool = None,
#         at: dict[str, str] = None,
#         before: dict[str, str] = None,
#         insert_only: bool = None,
#         comment: str = None,
#         **kwargs,
#     ):
#         super().__init__(**kwargs)
#         self._data = _ExternalTableStream(
#             name=name,
#             on_external_table=on_external_table,
#             owner=owner,
#             copy_grants=copy_grants,
#             at=at,
#             before=before,
#             insert_only=insert_only,
#             comment=comment,
#         )


@dataclass(unsafe_hash=True)
class _StageStream(ResourceSpec):
    name: str
    on_stage: str
    owner: Role = "SYSADMIN"
    copy_grants: bool = None
    comment: str = None


class StageStream(Resource):
    """
    -- Directory table
    CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
      <name>
      [ COPY GRANTS ]
      ON STAGE <stage_name>
      [ COMMENT = '<string_literal>' ]
    """

    resource_type = ResourceType.STREAM
    props = Props(
        copy_grants=FlagProp("copy grants"),
        on_stage=IdentifierProp("on stage", eq=False),
        comment=StringProp("comment"),
    )
    scope = SchemaScope()
    spec = _StageStream

    def __init__(
        self,
        name: str,
        on_stage: str,
        owner: str = "SYSADMIN",
        copy_grants: bool = None,
        comment: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._data = _StageStream(
            name=name,
            on_stage=on_stage,
            owner=owner,
            copy_grants=copy_grants,
            comment=comment,
        )
        self.requires(ResourcePointer(name=self._data.on_stage, resource_type=ResourceType.STAGE))


@dataclass(unsafe_hash=True)
class _ViewStream(ResourceSpec):
    name: str
    on_view: View
    owner: Role = "SYSADMIN"
    copy_grants: bool = None
    at: dict[str, str] = None
    before: dict[str, str] = None
    append_only: bool = None
    show_initial_rows: bool = None
    comment: str = None


class ViewStream(Resource):
    """
    CREATE [ OR REPLACE ] STREAM [IF NOT EXISTS]
      <name>
      [ COPY GRANTS ]
      ON VIEW <view_name>
      [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> | STREAM => '<name>' } ) ]
      [ APPEND_ONLY = TRUE | FALSE ]
      [ SHOW_INITIAL_ROWS = TRUE | FALSE ]
      [ COMMENT = '<string_literal>' ]
    """

    resource_type = ResourceType.STREAM
    props = Props(
        copy_grants=FlagProp("copy grants"),
        on_view=IdentifierProp("on view", eq=False),
        at=TimeTravelProp("at"),
        before=TimeTravelProp("before"),
        append_only=BoolProp("append_only"),
        show_initial_rows=BoolProp("show_initial_rows"),
        comment=StringProp("comment"),
    )
    scope = SchemaScope()
    spec = _ViewStream

    def __init__(
        self,
        name: str,
        on_view: str,
        owner: str = "SYSADMIN",
        copy_grants: bool = None,
        at: dict[str, str] = None,
        before: dict[str, str] = None,
        append_only: bool = None,
        show_initial_rows: bool = None,
        comment: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._data = _ViewStream(
            name=name,
            on_view=on_view,
            owner=owner,
            copy_grants=copy_grants,
            at=at,
            before=before,
            append_only=append_only,
            show_initial_rows=show_initial_rows,
            comment=comment,
        )
        self.requires(self._data.on_view)


StreamTypeMap = {
    StreamType.TABLE: TableStream,
    # StreamType.EXTERNAL_TABLE: ExternalTableStream,
    StreamType.STAGE: StageStream,
    StreamType.VIEW: ViewStream,
}


def _resolver(data: dict):
    if "on_table" in data:
        return TableStream
    # elif "on_external_table" in data:
    #     return ExternalTableStream
    elif "on_stage" in data:
        return StageStream
    elif "on_view" in data:
        return ViewStream
    # using this as a workaround because there may not be enough properties during a small change to disambiguate
    # really the different stream types should probably have seperate resource types.
    # Either that, or the resolver would need to look at the database to see what type of stream it is
    return TableStream


Resource.__resolvers__[ResourceType.STREAM] = _resolver
