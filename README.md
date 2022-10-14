# CChrome: Chrome driver that ensures load completion

**CChrome** is a Chrome web driver that provides a method that loads any given web page completely
in the current browser session.

## Examples

```python
from cchrome import CChrome

cchrome = CChrome()

# Usage of CChrome.get_with_page_completion() is the same as the Chrome.get()
# when optional parameters are left to assume their default values.
cchrome.get_with_page_completion('https://www.nytimes.com')

# Setting of optional parameters is to control the total amount of time allowed in trying to load the given page
# completely and the time allocated in polling for the loading state of the given page.
cchrome.get_with_page_completion('https://www.twitter.com', 3.0, 8.0)
```

## The get method with completion assurance

CChrome.**get_with_page_completion**(_url, page_load_timeout_multiplier=4.0, get_to_complete_timeout=10.0_)

### Parameters:

* **url** - The URL of the web page to be loaded
* **page_load_timeout_multiplier** - The multiplier used to set the total allowed page loading time, indirectly.
  The total allowed page loading time is the value of this parameter times
  the current page load timeout of this driver. I.e.,
  total allowed page loading time =
  page_load_timeout_multiplier * cchrome.timeouts.page_load
* **get_to_complete_timeout** - The total time allocated for polling for the loading state of the page to reach
  the state of "complete" since the Chrome.get() method returns after fetching
  the page. The value of this parameter should be no less than 5.

### Return:

This method returns the return of the last call to Chrome.get() that successfully loads the requested page completely.

### Raise:

This method raises **CChrome.CompletionTimeoutError** if the given page fails to be completely loaded within
the total allowed page loading time.
