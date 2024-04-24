# Run FastAPI Apps

```commandline
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
uvicorn main:app --host 0.0.0.0 --port 8004 --reload


cat<<EOF | sudo tee /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
  worker_connections 1024;
}

http {
  upstream fastapi {
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
  }

  server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name _;
    root /usr/share/nginx/html;

    ssl_certificate "/etc/nginx/tls/self.cert";
    ssl_certificate_key "/etc/nginx/tls/self.key";
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 10m;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    error_page 404 /404.html;
    location = /40x.html {
      # Ensure that this block has some configuration or is commented out
      # if it is not being used.
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
      # Ensure that this block has some configuration or is commented out
      # if it is not being used.
    }

    location / {
      proxy_pass http://fastapi;
    }
  } # This closes the server block
} # This closes the http block

EOF

