## Run fastapi apps
```commandline
uvicorn mall.main:app --host 0.0.0.0 --port 8002 --reload

uvicorn mall.main:app --host 0.0.0.0 --port 8003 --reload

uvicorn mall.main:app --host 0.0.0.0 --port 8004 --reload
```

## Configure nginx

```commandline
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
             proxy_pass http://fastapi;
         }


        }

}
EOF
```

## Reload nginx
```commandline
sudo nginx -s reload
```

## Browser
https://localhost:1081/docs

- Make some predictions and observe fastapi logs. Load balancer is expected to direct requests round robin manner.
