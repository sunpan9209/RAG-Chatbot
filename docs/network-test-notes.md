# Network and test execution notes

## Test run location

Tests were executed inside the container at `/workspace/RAG-Chatbot` using:

```bash
python -m unittest discover -s /workspace/RAG-Chatbot/tests
```

Result:

```
ss.s.s
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK (skipped=4)
```

## Network restrictions observed

Attempting to install dependencies from PyPI fails due to a proxy 403 restriction:

```bash
pip install -e /workspace/RAG-Chatbot
```

Error output:

```
Obtaining file:///workspace/RAG-Chatbot
  Installing build dependencies: started
  Installing build dependencies: finished with status 'error'
  error: subprocess-exited-with-error

  × installing build dependencies did not run successfully.
  │ exit code: 1
  ╰─> [7 lines of output]
      WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/setuptools/
      WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/setuptools/
      WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/setuptools/
      WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/setuptools/
      WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 403 Forbidden'))': /simple/setuptools/
      ERROR: Could not find a version that satisfies the requirement setuptools>=40.8.0 (from versions: none)
      ERROR: No matching distribution found for setuptools>=40.8.0
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'file:///workspace/RAG-Chatbot' when installing build dependencies
```
