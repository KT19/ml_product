# This repository is application of object detection.
Object detection tends to require a lot of computational resources.
This repo demonstrates implementing object detector in the server-side.
The clients send an image to the server and the results will be returned.
This transmission is realized by using socket programming.

## Example of demo
1. (Optional)
Modify ip address and port on the server if necessary.
The `config.py` contains such configures.

2. Run server-side code by:
```python
python3 server.py
```

3. Run client-side code by:
```python
python3 client.py
```
In default, the images captured by camera (used opencv's VideoCapture) are transmitted to the server.

### Code info
object detector is written in `object_detector.py`.

Socket programming is written in `server.py` (for receiving data from clients) and `utils.py` (for transmitting data to the server).
