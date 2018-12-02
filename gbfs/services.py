from gbfs.providers import systems_provider_remote_csv
from gbfs.client import GBFSClient
from gbfs.const import gbfs_systems_csv_fields


__all__ = ['SystemDiscoveryService']


class SystemDiscoveryService(object):
    """GBFS client discovery service"""

    _default_language = 'en'
    _client_cls = None
    _systems_provider = None
    _system_attrs = None

    def __init__(self, run_on_init=True):
        assert self._client_cls
        assert self._systems_provider
        assert self._system_attrs

        self._systems_cache = {}

        if run_on_init:
            self._get_and_cache_all_systems()

    def _get_and_cache_all_systems(self):
        try:
            systems = self._systems_provider.get_all()
        except:
            raise

        for system in systems:
            system_id = system.get(self._system_attrs.system_id)
            if system_id is None:
                raise RuntimeError('Unexpected systems data format.')
            self._systems_cache[system_id] = system


    @property
    def system_ids(self):
        if self._systems_cache:
            return list(self._systems_cache.keys())

    def system_information(self, system_id):
        return self._systems_cache.get(system_id)

    def instantiate_client(self, system_id, language=None):
        system = self._systems_cache.get(system_id)
        if system:
            system_url = system.get(self._system_attrs.auto_discovery_url)
            if system_url:
                try:
                    client = self._client_cls(system_url, language if language else self._default_language)
                except:
                    raise RuntimeError('Could not instantiate client with system url: {}'.format(system_url))
                return client

# Runtime config
SystemDiscoveryService._system_attrs = gbfs_systems_csv_fields
SystemDiscoveryService._client_cls = GBFSClient
SystemDiscoveryService._systems_provider = systems_provider_remote_csv
