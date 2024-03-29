- https://www.youtube.com/watch?v=wQcSql62zRo

```commandline
cd /etc/nginx

sudo mkdir tls

sudo openssl req -x509 -days 365 \
-nodes -newkey rsa:2048 \
-keyout /etc/nginx/tls/self.key \
-out /etc/nginx/tls/self.cert
```
## Port forwarding
1081 -> 443

## Configure for tls
- /etc/nginx/nginx.conf
```commandline
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
server {
        listen       443 ssl http2;
        listen       [::]:443 ssl http2;
        server_name  _;
        root         /usr/share/nginx/html;

        ssl_certificate "/etc/nginx/tls/self.cert";
        ssl_certificate_key "/etc/nginx/tls/self.key";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  10m;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
                location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
                location = /50x.html {
        }

        location / {
                proxy_pass http://127.0.0.1:8002;
        }
}
}
```

## Restart nginx service
```commandline
sudo systemctl restart nginx
```

## Access FastAPI with https
- Browser: https://127.0.0.1:1081/docs