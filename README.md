# HTTPlus

An HTTP asynchronous client.

[![Stable Version](https://img.shields.io/pypi/v/httplus?label=pypi)](https://pypi.org/project/httplus/)



## Instalation
```shell
pip install httplus
```

## Basic Usage
The simplest request using get method is showed below.
```python
import httplus
...
client = httplus.Client()
res = await client.get('http://someserver/api/collection')
print(res.status)
# 200
data = res.json()
# {...}
```
A request is executed by Client instance class. 
The Client class has get, post, put, delete, options, 
patch and head methods to do requests.


## Examples
### Sending data through POST request
```python
import httplus
...
data = {
    'name': 'Vink',
    'surname': 'Blaster'
}
client = httplus.Client()
res = await client.post('http://someserver/api/customers', data=data)
print(res.status)
# 200
```
The data parameter can be a dict, list or a binary object.
A dict or a list passed by data param will be interpreted like **JSON** format data.
If a binary data like a pdf or an image file is been sending,
a header content mime type need to be informed by headers param.

```python
import httplus
...
image = b'<some_image_binary>'
headers = {
    'Content-Type': 'image/png'
}
url = 'http://someserver/api/books'
...
client = httplus.Client()
res = await client.post(url=url, data=image, headers=headers)
print(res.status)
# 200
```
