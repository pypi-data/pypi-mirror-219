import enum
import logging
import typing as t
import warnings
from copy import copy

import httpx
import packaging.version
from httpx import URL

import deepchecks_llm_client
from deepchecks_llm_client.utils import maybe_raise

__all__ = ['API', 'EnvType', 'AnnotationType']

logger = logging.getLogger(__name__)

TAPI = t.TypeVar('TAPI', bound='API')


class EnvType(str, enum.Enum):
    PROD = "PROD"
    EVAL = "EVAL"


class AnnotationType(str, enum.Enum):
    GOOD = "good"
    BAD = "bad"
    UNKNOWN = "unknown"


class API:

    session: httpx.Client
    original_host: URL

    @classmethod
    def instantiate(cls: type[TAPI], host: str, token: t.Optional[str] = None) -> TAPI:
        headers = {'Authorization': f'Basic {token}'} if token else None
        return cls(session=httpx.Client(base_url=host, headers=headers, timeout=60))

    def __init__(self, session: httpx.Client):
        self.session = copy(session)
        self.original_host = self.session.base_url
        self.session.base_url = self.session.base_url.join('/api/v1')

        try:
            backend_version = packaging.version.parse(self.retrieve_backend_version())
            client_version = packaging.version.parse(deepchecks_llm_client.__version__)
        except packaging.version.InvalidVersion:
            warnings.warn(
                'Not able to compare backend and client versions, '
                'backend or client use incorrect or legacy versioning schema.'
            )
        else:
            if backend_version.major != client_version.major:
                warnings.warn(
                    'You are using an old, potentially incompatible with the current API, client version. '
                    'Upgrade "deepchecks_client" version by running:\n'
                    '>> pip install -U deepchecks_client'
                )

    def retrieve_backend_version(self) -> str:
        """Return current active backend version.

        Returns
        -------
        str : backend version string
        """
        payload = maybe_raise(
            self.session.get('backend-version'),
            msg='Server not available.\n{error}'
        ).json()
        return payload['version']

    def load_openai_data(self,
                         data: t.List[t.Dict[str, t.Any]],
                         app_name: str,
                         version_name: str,
                         env_type: EnvType
                         ) -> t.Optional[httpx.Response]:
        try:
            return maybe_raise(self.session.post('openai-load', json=data,
                                                 params={'app_name': app_name,
                                                         'version_name': version_name,
                                                         'env_type': env_type.value}))
        except Exception as ex:
            logger.warning(f'Failed to send openai data to deepchecks, message: {str(ex)}')

    def annotate(self,
                 ext_interaction_id: str,
                 annotation: AnnotationType
                 ) -> t.Optional[httpx.Response]:
        try:
            return maybe_raise(self.session.post('annotations', json={"ext_interaction_id": ext_interaction_id,
                                                                      "value": annotation.value}))
        except Exception as ex:
            logger.warning(f'Failed to send annotation data to deepchecks, message: {str(ex)}')

    def get_application(self,
                 app_name: str,
                 ) -> t.Optional[httpx.Response]:
        try:
            return maybe_raise(self.session.get('applications', params={"name": [app_name]})).json()
        except Exception as ex:
            logger.warning(f'Failed to get application name: {app_name} from deepchecks, message: {str(ex)}')
            return []


