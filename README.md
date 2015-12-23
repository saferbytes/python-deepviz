# python-deepviz
python-deepviz is a wrapper for deepviz.com REST APIs

# usage

To use Deepviz API sdk you will need an API key you can get by
subscribing the service at https://account.deepviz.com/register/

# Sandbox SDK API

To upload a sample:

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
sbx.upload_sample(path="path\\to\\file.exe", apikey="my-api-key", rescan=False)
```