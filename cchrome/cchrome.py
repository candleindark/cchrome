from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
import polling2


class CChrome(Chrome):
    """
    An instance of this class represents a Chrome web driver that ensures a page loaded by its get method loads fully
    """

    def __init__(self, *args, **kwargs):
        super(CChrome, self).__init__(*args, **kwargs)

        # Set timeout for page loading
        self.set_page_load_timeout(20)

    def get(self, url):
        def success(_):
            try:
                # Wait for and reaffirm that the page is loaded completely
                polling2.poll(
                    target=self.execute_script,
                    step=0.05,
                    args=('return document.readyState',),
                    timeout=8.0,
                    check_success=lambda doc_ready_state: doc_ready_state == 'complete'
                )
            except polling2.TimeoutException:
                return False
            else:
                return True

        try:
            ret = polling2.poll(
                target=super().get,
                step=0.5,
                args=(url,),
                timeout=120.0,
                check_success=success,
                ignore_exceptions=(TimeoutException,)
            )
        except polling2.TimeoutException:
            raise RuntimeError(f'{url} has failed to load completely.')
        else:
            return ret
