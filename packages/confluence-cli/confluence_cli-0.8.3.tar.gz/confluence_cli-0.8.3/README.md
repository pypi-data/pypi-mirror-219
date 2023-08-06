# confluence-cli

confluence-cli is a convenient wrapper module for python atlassian confluence original package.

## confluence-cli installation

```shell
# Desde la raiz del repositorio
python3 -m pip install  confluence-cli
```

## Examples

```python

params = {
        "baseURL": "http://confluence:8090",
        "user": "myuser",
        "password": "mypass",
        "proxies": {
            "http": "",
            "https": ""
        },
        "verify_ssl": False
    }

confluence_api = ConfluenceWrapper(params)
# This class method, for example, is not available in original atlassian confluence module.
confluence_api.add_content_restrictions("3407893",["read","update"],group_name, "group")
# This class method, for example, is not available in original atlassian confluence module.
confluence_api.add_space_permissions_rpc(space_key="ds",permissions=["SETSPACEPERMISSIONS","EXPORTSPACE"],entity_name=group_name)
    

```
