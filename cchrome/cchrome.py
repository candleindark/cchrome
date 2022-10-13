import polling2
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome


class CompletionTimeoutError(Exception):
    pass


class CChrome(Chrome):
    """
    An instance of this class represents a Chrome web driver that provides a method that loads any given web page
    completely in the current browser session.
    """

    def __init__(self, *args, **kwargs):
        super(CChrome, self).__init__(*args, **kwargs)

    def get_with_page_completion(self, url,
                                 page_load_timeout_multiplier: float = 4.0, get_to_complete_timeout: float = 10.0):
        """
        Load a web page at a given URL in the current browser session with the assurance of the completion of loading

        .. note:: This method assures the loading of the specified web page to be complete by polling for the loading
                  state of the page as described in
                  https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState. Multiple attempts to load the
                  web page may be made, using the Chrome.get() method, until the page is completely loaded successfully
                  or the time elapsed is greater than the allowed page loading time.

        :param url: The URL of the web page to be loaded
        :param page_load_timeout_multiplier: The multiplier used to set the total allowed page loading time.
                                             The total allowed page loading time is the value of this parameter times
                                             the current page load timeout of this driver. I.e.,
                                             total allowed page loading time =
                                             page_load_timeout_multiplier * chrome.timeouts.page_load
        :param get_to_complete_timeout: The total time allocated for polling for the loading state of the page to reach
                                        the state of "complete" since the Chrome.get() method returns after fetching
                                        the page. The value of this parameter should be no less than 5.
        :return: The return of the last call to Chrome.get() that successfully loads the requested page completely
        :raise: CompletionTimeoutError if page fails to be completely loaded within the total allowed page loading time
        """
        if get_to_complete_timeout < 5.0:
            raise ValueError(f'The value of get_to_complete_timeout is too small. Try a value no less than 5.')
        if self.timeouts.page_load * (page_load_timeout_multiplier - 1) < get_to_complete_timeout:
            raise ValueError(f'page_load_timeout_multiplier is too small. Try a greater value.')

        allowed_page_load_time = self.timeouts.page_load * page_load_timeout_multiplier

        def success(_):
            polling_lapse = 0.05
            try:
                # Wait for and reaffirm that the page is loaded completely
                polling2.poll(
                    target=self.execute_script,
                    step=polling_lapse,
                    args=('return document.readyState;',),
                    timeout=get_to_complete_timeout,
                    check_success=lambda doc_ready_state: doc_ready_state == 'complete'
                )
            except polling2.TimeoutException:
                return False
            else:
                return True

        try:
            ret = polling2.poll(
                target=super().get,
                step=0,  # No wait time is needed here because success() incurs wait time between attempts
                args=(url,),
                timeout=allowed_page_load_time,
                check_success=success,
                ignore_exceptions=(TimeoutException,)
            )
        except polling2.TimeoutException:
            raise CompletionTimeoutError(f'{url} has failed to load completely within {allowed_page_load_time} secs.')
        else:
            return ret
