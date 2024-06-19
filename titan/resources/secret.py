from dataclasses import dataclass, field

from .resource import Resource, ResourceSpec, ResourceNameTrait
from .role import Role
from ..resource_name import ResourceName
from ..enums import ParseableEnum, ResourceType
from ..scope import SchemaScope
from ..props import (
    EnumProp,
    Props,
    StringProp,
    StringListProp,
)


class SecretType(ParseableEnum):
    OAUTH2 = "OAUTH2"
    PASSWORD = "PASSWORD"
    GENERIC_STRING = "GENERIC_STRING"


# @dataclass(unsafe_hash=True)
# class _Secret(ResourceSpec):
#     name: ResourceName
#     type: SecretType
#     api_authentication: str
#     oauth_scopes: list[str] = None
#     oauth_refresh_token: str = None
#     oauth_refresh_token_expiry_time: str = None
#     username: str = None
#     password: str = None
#     secret_string: str = None
#     comment: str = None
#     owner: Role = "SYSADMIN"

#     def __post_init__(self):
#         super().__post_init__()
#         if self.type == SecretType.OAUTH2 and not self.api_authentication:
#             raise ValueError("api_authentication must be set when type is OAUTH2")
#         if self.type != SecretType.OAUTH2 and self.api_authentication:
#             raise ValueError("api_authentication must not be set when type is not OAUTH2")


@dataclass(unsafe_hash=True)
class _PasswordSecret(ResourceSpec):
    name: ResourceName
    secret_type: SecretType = SecretType.PASSWORD
    username: str = None
    password: str = field(default_factory=None, metadata={"fetchable": False})
    comment: str = None
    owner: Role = "SYSADMIN"


class PasswordSecret(ResourceNameTrait, Resource):
    """
    Description:
        A Secret defines a set of sensitive data that can be used for authentication or other purposes.
        This class defines a password secret.

    Snowflake Docs:
        https://docs.snowflake.com/en/sql-reference/sql/create-secret

    Fields:
        name (string, required): The name of the secret.
        username (string): The username for the secret.
        password (string): The password for the secret.
        comment (string): A comment for the secret.
        owner (string or Role): The owner of the secret. Defaults to SYSADMIN.

    Python:

        ```python
        secret = PasswordSecret(
            name="some_secret",
            username="some_username",
            password="some_password",
            comment="some_comment",
            owner="SYSADMIN",
        )
        ```

    Yaml:

        ```yaml
        secrets:
          - name: some_secret
            secret_type: PASSWORD
            username: some_username
            password: some_password
            comment: some_comment
            owner: SYSADMIN
        ```
    """

    resource_type = ResourceType.SECRET
    props = Props(
        secret_type=EnumProp("type", SecretType),
        username=StringProp("username"),
        password=StringProp("password"),
        comment=StringProp("comment"),
    )
    scope = SchemaScope()
    spec = _PasswordSecret

    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        comment: str = None,
        owner: str = "SYSADMIN",
        **kwargs,
    ):
        kwargs.pop("secret_type", None)
        super().__init__(name, **kwargs)
        self._data: _PasswordSecret = _PasswordSecret(
            name=self._name,
            username=username,
            password=password,
            comment=comment,
            owner=owner,
        )


@dataclass(unsafe_hash=True)
class _GenericSecret(ResourceSpec):
    name: ResourceName
    secret_type: SecretType = SecretType.GENERIC_STRING
    secret_string: str = field(default_factory=None, metadata={"fetchable": False})
    comment: str = None
    owner: Role = "SYSADMIN"


class GenericSecret(ResourceNameTrait, Resource):
    """
    Description:
        A Secret defines a set of sensitive data that can be used for authentication or other purposes.
        This class defines a generic secret.

    Snowflake Docs:
        https://docs.snowflake.com/en/sql-reference/sql/create-secret

    Fields:
        name (string, required): The name of the secret.
        secret_string (string): The secret string.
        comment (string): A comment for the secret.
        owner (string or Role): The owner of the secret. Defaults to SYSADMIN.

    Python:

        ```python
        secret = GenericSecret(
            name="some_secret",
            secret_string="some_secret_string",
            comment="some_comment",
            owner="SYSADMIN",
        )
        ```

    Yaml:

        ```yaml
        secrets:
          - name: some_secret
            secret_type: GENERIC_STRING
            secret_string: some_secret_string
            comment: some_comment
            owner: SYSADMIN
        ```
    """

    resource_type = ResourceType.SECRET
    props = Props(
        secret_type=EnumProp("type", SecretType),
        secret_string=StringProp("secret_string"),
        comment=StringProp("comment"),
    )
    scope = SchemaScope()
    spec = _GenericSecret

    def __init__(
        self,
        name: str,
        secret_string: str,
        comment: str = None,
        owner: str = "SYSADMIN",
        **kwargs,
    ):
        kwargs.pop("secret_type", None)
        super().__init__(name, **kwargs)
        self._data: _GenericSecret = _GenericSecret(
            name=self._name,
            secret_string=secret_string,
            comment=comment,
            owner=owner,
        )


# class Secret(ResourceNameTrait, Resource):
#     """
#     Description:
#         A Secret defines a set of sensitive data that can be used for authentication or other purposes.

#     Snowflake Docs:
#         https://docs.snowflake.com/en/sql-reference/sql/create-secret

#     Fields:
#         name (string, required): The name of the secret.
#         type (string or SecretType, required): The type of the secret.
#         api_authentication (string): The security integration name for API authentication.
#         oauth_scopes (list): The OAuth scopes for the secret.
#         oauth_refresh_token (string): The OAuth refresh token.
#         oauth_refresh_token_expiry_time (string): The expiry time of the OAuth refresh token.
#         username (string): The username for the secret.
#         password (string): The password for the secret.
#         secret_string (string): The secret string.
#         comment (string): A comment for the secret.
#         owner (string or Role): The owner of the secret. Defaults to SYSADMIN.

#     Python:

#         ```python
#         secret = Secret(
#             name="some_secret",
#             type="OAUTH2",
#             api_authentication="some_security_integration",
#             oauth_scopes=["scope1", "scope2"],
#             oauth_refresh_token="some_refresh_token",
#             oauth_refresh_token_expiry_time="some_expiry_time",
#             username="some_username",
#             password="some_password",
#             secret_string="some_secret_string",
#             comment="some_comment",
#             owner="SYSADMIN",
#         )
#         ```

#     Yaml:

#         ```yaml
#         secrets:
#           - name: some_secret
#             type: OAUTH2
#             api_authentication: some_security_integration
#             oauth_scopes:
#               - scope1
#               - scope2
#             oauth_refresh_token: some_refresh_token
#             oauth_refresh_token_expiry_time: some_expiry_time
#             username: some_username
#             password: some_password
#             secret_string: some_secret_string
#             comment: some_comment
#             owner: SYSADMIN
#         ```
#     """

#     resource_type = ResourceType.SECRET
#     props = Props(
#         type=EnumProp("type", SecretType),
#         api_authentication=StringProp("api_authentication"),
#         oauth_scopes=StringListProp("oauth_scopes", parens=True),
#         oauth_refresh_token=StringProp("oauth_refresh_token"),
#         oauth_refresh_token_expiry_time=StringProp("oauth_refresh_token_expiry_time"),
#         username=StringProp("username"),
#         password=StringProp("password"),
#         secret_string=StringProp("secret_string"),
#         comment=StringProp("comment"),
#     )
#     scope = SchemaScope()
#     spec = _Secret

#     def __init__(
#         self,
#         name: str,
#         type: SecretType,
#         api_authentication: str = None,
#         oauth_scopes: list[str] = None,
#         oauth_refresh_token: str = None,
#         oauth_refresh_token_expiry_time: str = None,
#         username: str = None,
#         password: str = None,
#         secret_string: str = None,
#         comment: str = None,
#         owner: str = "SYSADMIN",
#         **kwargs,
#     ):
#         super().__init__(name, **kwargs)
#         self._data: _Secret = _Secret(
#             name=self._name,
#             type=type,
#             api_authentication=api_authentication,
#             oauth_scopes=oauth_scopes,
#             oauth_refresh_token=oauth_refresh_token,
#             oauth_refresh_token_expiry_time=oauth_refresh_token_expiry_time,
#             username=username,
#             password=password,
#             secret_string=secret_string,
#             comment=comment,
#             owner=owner,
#         )


SecretMap = {
    SecretType.PASSWORD: PasswordSecret,
    # SecretType.OAUTH2: OAuth2Secret,
    SecretType.GENERIC_STRING: GenericSecret,
}


def _resolver(data: dict):
    return SecretMap[SecretType(data["secret_type"])]


Resource.__resolvers__[ResourceType.SECRET] = _resolver
