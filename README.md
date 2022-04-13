# PiDashBackEnd

[![CodeFactor](https://www.codefactor.io/repository/github/gingertronmk1/pidashbackend/badge)](https://www.codefactor.io/repository/github/gingertronmk1/pidashbackend)

This is a Flask-based simple web server that's designed to feed data to the [PiDashFrontEnd](https://github.com/GingertronMk1/PiDashFrontEnd).
It uses `psutil` to get system parameters (CPU load, memory usage, disk usage, etc), and `requests` to get information from [Transmission's](https://transmissionbt.com/) RPC client.
It packages all that up into a lovely little set of endpoints to which the aforementioned front-end is attached.

### Current Routes

- `/cpu`
- `/memory`
- `/disk`
- `/temperatures`
- `/transmission`
