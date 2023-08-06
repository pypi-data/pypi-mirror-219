from typing import Callable
from concurrent.futures import ThreadPoolExecutor


class OssitRequest:
    def __init__(self, ossit_api_requestor: Callable[..., any], **kwargs):
        self.ossit_api_requestor = ossit_api_requestor
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.ossit_api_requestor(**self.kwargs)


def send_threaded_requests(*ossit_requests: OssitRequest) -> None:

    # Create an executor and start the request in a new thread
    executor = ThreadPoolExecutor(max_workers=5)
    for ossit_request in ossit_requests:
        executor.submit(ossit_request)

    # Shutdown the executor. This doesn't block the running request
    executor.shutdown(wait=False)

