import logging
import time
import typing as t

import openai
from deepchecks_llm_client.api import API, EnvType

logger = logging.getLogger(__name__)

class OpenAIInstrumentor:

    def __init__(self, api: API, app_name: str, version_name: str,env_type: EnvType):
        self.api = api
        self.app_name = app_name
        self.version_name = version_name
        self.env_type = env_type
        self._tags = dict()

        self.openai_version = "0.0.0"
        try:
            from importlib import metadata
            self.openai_version = metadata.version('openai')
        except Exception as ex:
            pass

    def set_context(self, app_name, version_name, env_type):
        self.app_name = app_name
        self.version_name = version_name
        self.env_type = env_type

    @property
    def tags(self) -> t.Dict[str, t.Any]:
        return self._tags

    @tags.setter
    def tags(self, tags: t.Dict[str, t.Any]):
        self._tags = tags

    @staticmethod
    def _patched_call(original_fn, patched_fn):
        def _inner_patch(*args, **kwargs):
            return patched_fn(original_fn, *args, **kwargs)
        return _inner_patch

    def patcher_create(self, original_fn, *args, **kwargs):

        self._before_run_log_print(args, kwargs, original_fn)

        timestamp = time.time()
        result = original_fn(*args, **kwargs)
        time_delta = time.time() - timestamp

        self._after_run_actions(args, kwargs, original_fn, result, time_delta)

        return result

    async def patcher_acreate(self, original_fn, *args, **kwargs):

        self._before_run_log_print(args, kwargs, original_fn)

        timestamp = time.time()
        result = await original_fn(*args, **kwargs)
        time_delta = time.time() - timestamp

        self._after_run_actions(args, kwargs, original_fn, result, time_delta)

        return result

    def _after_run_actions(self, args, kwargs, original_fn, result, time_delta):
        logger.debug(
            f"Finished running function: '{original_fn.__qualname__}'. result: {result}, time delta: {time_delta}")
        event_dict = {
            "request": {"func_name": original_fn.__qualname__, "args": args, "kwargs": kwargs},
            "response": result.to_dict_recursive(),
            "runtime_data": {"response_time": time_delta, "openai_version": self.openai_version},
            "user_data": self.tags
        }
        self.api.load_openai_data(data=[event_dict], app_name=self.app_name,
                                  version_name=self.version_name, env_type=self.env_type)
        logger.debug(f"Reported event dictionary:\n{event_dict}")

    @staticmethod
    def _before_run_log_print(args, kwargs, original_fn):
        logger.debug(f"Running the original function: '{original_fn.__qualname__}'. args:{args}; kwargs: {kwargs}")

    def perform_patch(self):
        try:
            openai.ChatCompletion.acreate = self._patched_call(
                openai.ChatCompletion.acreate, self.patcher_acreate
            )
        except AttributeError:
            pass

        try:
            openai.ChatCompletion.create = self._patched_call(
                openai.ChatCompletion.create, self.patcher_create
            )
        except AttributeError:
            pass

        try:
            openai.Completion.acreate = self._patched_call(
                openai.Completion.acreate, self.patcher_acreate
            )
        except AttributeError:
            pass

        try:
            openai.Completion.create = self._patched_call(
                openai.Completion.create, self.patcher_create
            )
        except AttributeError:
            pass

