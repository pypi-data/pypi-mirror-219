from fluvii.auth import SaslScramClientConfig, GlueRegistryClientConfig
from fluvii.producer import Producer
from fluvii.schema_registry import GlueSchemaRegistryClient

from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.yaml_parser import load_yaml_fp


def gtfo_producer(topic_schema_dict):
    cluster_config = load_yaml_fp(env_vars()['NU_KAFKA_CLUSTERS_CONFIGS_YAML'])[load_yaml_fp(env_vars()['NU_TOPIC_CONFIGS_YAML'])[list(topic_schema_dict.keys())[0]]['cluster']]
    auth = SaslScramClientConfig(username=cluster_config['username'], password=cluster_config['password'], mechanisms= 'SCRAM-SHA-512')
    auth_glue = GlueRegistryClientConfig(
            env_vars()["FLUVII_SCHEMA_REGISTRY_ACCESS_KEY_ID"],
            env_vars()["FLUVII_SCHEMA_REGISTRY_SECRET_ACCESS_KEY"],
            env_vars()["FLUVII_SCHEMA_REGISTRY_REGION_NAME"],
            env_vars()["FLUVII_SCHEMA_REGISTRY_REGISTRY_NAME"]
    )
    return Producer(
        cluster_config['url'],
        schema_registry=GlueSchemaRegistryClient(auth_glue),
        client_auth_config=auth,
        topic_schema_dict=topic_schema_dict,
    )
