## Start FastAPI
```commandline
uvicorn mall.main:app --host 0.0.0.0 --port 8002 --reload
```

## Install NGINX
```commandline
sudo yum -y install epel-release
sudo yum -y install nginx
```

## Backup nginx.cofg
```commandline
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.original
```

## Start nginx service
```commandline
sudo systemctl start nginx
```

## Check service
```commandline
 sudo ps aux | grep nginx
```
- Output
```commandline
root      1855  0.0  0.0  39308   936 ?        Ss   23:50   0:00 nginx: master process /usr/sbin/nginx
nginx     1856  0.0  0.0  39696  1812 ?        S    23:50   0:00 nginx: worker process
nginx     1857  0.0  0.0  39696  1812 ?        S    23:50   0:00 nginx: worker process
train     1859  0.0  0.0 112812   980 pts/0    S+   23:50   0:00 grep --color=auto nginx
```

## Port forwarding
- 1080 -> 80

## NGINX UI
- Browser: http://localhost:1080/


## Allow nginx config permissions
```commandline
sudo setenforce permissive
```
- Make it permanent
  - sudo vim /etc/sysconfig/selinux
```commandline
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=permissive
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

```
## Configure nginx as reverse proxy
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
        listen 80;
        server_name 127.0.0.1;

        location / {
                proxy_pass http://127.0.0.1:8002;
        }
}
}
```

## Reload nginx
```commandline
sudo nginx -s reload
```

## Access FastAPI through NGINX
- Browser: http://localhost:1080/docs
- You must see swagger ui



