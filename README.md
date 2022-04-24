# PiDashBackEnd

[![CodeFactor](https://www.codefactor.io/repository/github/gingertronmk1/pidashbackend/badge)](https://www.codefactor.io/repository/github/gingertronmk1/pidashbackend)

This is a FastAPI-based simple web server that's designed to feed data to the [PiDashFrontEnd](https://github.com/GingertronMk1/PiDashFrontEnd).
It uses `psutil` to get system parameters (CPU load, memory usage, disk usage, etc), and `requests` to get information from [Transmission's](https://transmissionbt.com/) RPC client.
It packages all that up into a lovely little set of endpoints to which the aforementioned front-end is attached.

### To use this with the above linked front end

Set up your nginx file as follows:

```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/html;

	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		try_files $uri $uri/ =404;
	}

  location /dash-api/ {
    proxy_pass <BACKEND_URL>/;
  }

}
```
Where `<BACKEND_URL>` is the url of this application, normally with FastAPI `http://localhost:8000/`.
This file on a Raspberry Pi is located at `/etc/nginx/sites-available/default`.
