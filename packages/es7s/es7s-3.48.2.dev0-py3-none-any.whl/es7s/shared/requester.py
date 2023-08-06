# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import requests

from . import get_logger
from .exception import DataCollectionError
from .threads import ThreadSafeCounter
import threading as th
import typing as t


class Requester:
    DEFAULT_TIMEOUT = 10

    network_request_id = ThreadSafeCounter()

    def __init__(self, network_req_event: th.Event = None):
        self._network_req_event: th.Event = network_req_event or th.Event()

    def make_request(
        self,
        url: str,
        timeout: float = DEFAULT_TIMEOUT,
        request_fn: t.Callable[[], requests.Response] = None,
        log_response_body: bool = True,
    ) -> requests.Response:
        logger = get_logger()
        try:
            request_id = self.network_request_id.next()
            self._network_req_event.set()
            logger.log_http_request(request_id, url)
            if not request_fn:
                request_fn = lambda: requests.get(url, timeout=timeout)
            response = request_fn()
            logger.log_http_response(request_id, response, with_body=log_response_body)
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
            raise DataCollectionError()
        except requests.RequestException as e:
            logger.exception(e)
            raise DataCollectionError()
        finally:
            self._network_req_event.clear()

        if not response.ok:
            logger.warning(f"Weather fetching failed: HTTP {response.status_code}")
            raise DataCollectionError()

        logger.trace(response.text, "Remote service response")
        return response
