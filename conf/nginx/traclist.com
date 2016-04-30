server {
  server_name *.xploras.xyz www.xploras.xyz m.xploras.xyz xploras.xyz;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/asset-management/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }

  access_log        /var/log/nginx/asset/main.access.log;
  error_log         /var/log/nginx/asset/main.error.log;

  location /static {
    alias                    /opt/asset-management/static;
    add_header              Cache-Control public;
  }

  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    uwsgi_pass unix:///tmp/main.sock;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }
}


server {
  server_name api.xploras.xyz;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/asset-management/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }

  location /static {
    alias                    /opt/asset-management/static;
    add_header              Cache-Control public;
  }

  access_log        /var/log/nginx/asset/api.access.log;
  error_log         /var/log/nginx/asset/api.error.log;

  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    uwsgi_pass unix:///tmp/api.sock;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }

}