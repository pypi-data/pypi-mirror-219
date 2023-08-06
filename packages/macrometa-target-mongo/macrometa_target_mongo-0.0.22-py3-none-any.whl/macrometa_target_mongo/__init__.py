#
# Copyright (c) 2023 Macrometa Corp All rights reserved.
#

import pkg_resources
from c8connector import C8Connector, Sample, ConfigAttributeType, Schema
from c8connector import ConfigProperty


class MongoDBTargetConnector(C8Connector):
    """MongoDBTargetConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "MongoDB"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-target-mongo"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_target_mongo').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "target"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Send data into a MongoDB collection."

    def logo(self) -> str:
        """Returns the logo image for the connector."""
        return ""

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        return []

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        return []

    def reserved_keys(self) -> list[str]:
        """List of reserved keys for the connector."""
        return []

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('host', 'Host', ConfigAttributeType.STRING, True, False,
                           description='MongoDB host.',
                           placeholder_value='mongodb_host'),
            ConfigProperty('port', 'Port', ConfigAttributeType.INT, False, False,
                           description='MongoDB port.',
                           default_value='27017'),
            ConfigProperty('user', 'Username', ConfigAttributeType.STRING, True, False,
                           description='MongoDB user.',
                           placeholder_value='mongo'),
            ConfigProperty('password', 'Password', ConfigAttributeType.PASSWORD, True, False,
                           description='MongoDB password.',
                           placeholder_value='password'),
            ConfigProperty('auth_database', 'Auth Database', ConfigAttributeType.STRING, True, False,
                           description='MongoDB authentication database.',
                           default_value='admin'),
            ConfigProperty('database', 'Database', ConfigAttributeType.STRING, True, True,
                           description='MongoDB database name.',
                           placeholder_value='mongo'),
            ConfigProperty('target_collection', 'Target Collection', ConfigAttributeType.STRING, True, True,
                           description="Target collection name.",
                           placeholder_value='my_collection'),
            ConfigProperty('hard_delete', 'Hard Delete', ConfigAttributeType.BOOLEAN, False, False,
                           description='When `hard_delete` option is true then the documents which are deleted from '
                                       'the source will also be deleted from MongoDB. It is achieved by continuously checking '
                                       'the `_SDC_DELETED_AT` metadata attribute sent by the source connector.',
                           default_value='false'),
            ConfigProperty('srv', 'Enable Srv', ConfigAttributeType.BOOLEAN, False, False,
                           description='Uses a `mongodb+srv` protocol to connect. Disables the usage of `port` '
                                       'argument if set to `True.`',
                           default_value='false'),
            ConfigProperty('replica_set', 'Replica Set', ConfigAttributeType.STRING, False, False,
                           description='Name of replica set.',
                           placeholder_value='replica'),
            ConfigProperty('direct_connection', 'Direct Connection', ConfigAttributeType.BOOLEAN, False, False,
                           description='Specifies whether to connect directly to the specified MongoDB host as a standalone '
                                       'or connect to the entire replica set of which the given MongoDB host is a part.',
                           default_value='false'),
            ConfigProperty('ssl', 'Use SSL', ConfigAttributeType.BOOLEAN, False, False,
                           description='Can be set to true to connect using SSL.',
                           default_value='false'),
            ConfigProperty('verify_mode', 'Verify Mode', ConfigAttributeType.BOOLEAN, False, False,
                           description='Default SSL verify mode.',
                           default_value='true'),
            ConfigProperty('tls_ca_file', 'SSL/TLS CA Certificate', ConfigAttributeType.FILE, False, False,
                           description='Specific CA certificate in PEM string format. This is most often the case '
                                       'when using `self-signed` server certificate.',
                           placeholder_value="my_ca_certificate"),
            ConfigProperty('tls_certificate_key_file', 'SSL/TLS Client Certificate', ConfigAttributeType.FILE, False, False,
                           description='Specific client certificate in PEM string format. If the private key for the client '
                                       'certificate is stored in a separate file, it should be concatenated with the certificate file.',
                           placeholder_value="my_client_certificate"),
            ConfigProperty('tls_certificate_key_file_password', 'SSL/TLS Client Key Password', ConfigAttributeType.PASSWORD, False, False,
                           description='If the private key contained in the certificate keyfile is encrypted, users can provide a '
                                       'password or passphrase to decrypt the encrypted private keys.',
                           placeholder_value="my_client_key_password"),
            ConfigProperty('batch_size_rows', 'Batch Size', ConfigAttributeType.INT, False, False,
                           description='Maximum number of rows inserted per batch.',
                           default_value='1000'),
            ConfigProperty('batch_flush_interval', 'Batch Flush Interval (Seconds)',
                           ConfigAttributeType.INT, False, False,
                           description='Time between batch flush executions.',
                           default_value='60'),
            ConfigProperty('batch_flush_min_time_gap', 'Batch Flush Minimum Time Gap (Seconds)',
                           ConfigAttributeType.INT, False, False,
                           description='Minimum time gap between two batch flush tasks.',
                           default_value='60'),
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return []
