# Proxy Server on Python

This proxy modify content of site https://lifehacker.ru.
The modification is to add emotions after each six-letter word.
Emoji is sequentially selected from the given list.


### Requirements
pip and Python version 3.6.9 or higher should be installed
Also need to install requirements

```bash
pip install -r requirements.txt
```
###  Usage
Run the proxy:
```bash
python3 proxy-server.py
```
Also, need the set proxy server address in your browser
Default address is `127.0.0.1:8080`


Example of result:
![Test 1](docs/screenshot.png)
