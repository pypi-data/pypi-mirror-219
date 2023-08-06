# loggerr [![](https://img.shields.io/pypi/v/loggerr?style=flat-square)](https://pypi.org/project/loggerr/) [![](https://img.shields.io/static/v1?label=github&message=python-loggerr&labelColor=black&color=3572a5&style=flat-square&logo=github)](https://github.com/fiverr/python-loggerr) [![](https://circleci.com/gh/fiverr/python-loggerr.svg?style=svg)](https://circleci.com/gh/fiverr/python-loggerr)

## Zero configuration JSON logger(r)


```py
from loggerr import Loggerr

logger = Loggerr("warn")

logger.info("Something going as expected", { "host": socket.gethostname() }) # ignored
logger.warn("Something must have gone terribly wrong") # sent

except Exception as e:
    logger.error(e, { request: "this was the request" })
```

### Log level
Create logger instance with a minimal log level

Log levels are (respectively):
- debug
- verbose
- info
- warn
- error
- critical

For example, a logger with log level "warn" will only print logs with level "warn", "error", or "critical".

### Synonyms
A couple of function synonyms have been placed to your convenience:

| function | will log with level
| - | -
| `logger.log(...)` | "info"
| `logger.warning(...)` | "warn"
| `logger.fatal(...)` | "critical"
| `logger.panic(...)` | "critical"

### Arguments
**Create**: Loggerr class accepts one or two arguments:

1. {string} Case insensitive name of **minimal** log level. defaults to 'info'
2. {dictionary} {'Key':'Value'} pairs, optional. Persistent enrichment fields for all log records

```py
logger = Loggerr(os.environ["LOG_LEVEL"], { "host": socket.gethostname() })
```

**Send**:Logger functions accept one or two arguments:

1. {any} Record's "message" field. Traditionally this would be a string or an exception.
2. {dictionary} {'Key':'Value'} pairs, optional. Values should be JSON serializable

```py
logger.info("something, something", { dark: "side" })
```
