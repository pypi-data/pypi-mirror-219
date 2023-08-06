from typing import Callable
from concurrent.futures import ThreadPoolExecutor


def send_non_blocking_request(ossit_request: Callable[..., any], **callable_kwargs) -> None:

    def make_request(ossit_request: Callable[..., any], **callable_kwargs) -> None:
        ossit_request(**callable_kwargs)

    # Create an executor and start the request in a new thread
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(make_request, ossit_request, **callable_kwargs)
    # Shutdown the executor. This doesn't block the running request
    executor.shutdown(wait=False)

