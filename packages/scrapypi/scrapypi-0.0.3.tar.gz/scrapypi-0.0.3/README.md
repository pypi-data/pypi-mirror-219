**scrapypi is used to get pypi package information using python.**

scrapypi can be used to get package version, name, licence, author, summary and package download statistics.

**Insallation**

> python -m pip install scrapypi

**Usage**  
Type **scrapypi** in terminal or command prompt to scrapypi file for getting downloads statistics. scrapypi can also be used in code.

```bash
$ scrapypi
```

Below are examples and functions and classes in scrapypi for data fetching.

```python
from scrapypi import info, stats, licence

# Get package information. You can either get information using package name or package pypi url.

info(<package_name>) # returns a dictionary of information.

# Get package full statistics, including download values everyday of package upload, date and number of downloads.

statistics = stats(<package_name>)

statistics.dataset() # get daily download counts of package since first day of release.

statistics.get_total() # get total number of downloads since first day of package release.
```

You can also get package name and version using the version function.

```python
from scrapypi import version

version(<package_name>) # returns package name and version in a tuple. (name, version)
```

> Use the version function if you need to get those information fast. But i recommend using the info function.

Use the **main()** function to run the scrapypi script for statistics fetcher.
