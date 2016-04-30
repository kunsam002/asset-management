
upstream web_cluster_main {

  least_conn;  
  server  app1.traclist.com:8080;
  server  app2.traclist.com:8080;
}

server {
  server_name lb.traclist.com;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/Traclist/traclist/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }

  access_log        /var/log/nginx/traclist/main1.access.log;
  error_log         /var/log/nginx/traclist/main1.error.log;


  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    proxy_pass http://web_cluster_main;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }
}

upstream web_cluster_admin {

  least_conn;
  server  app1.traclist.com:8081;
  server  app2.traclist.com:8081;
}

server {
  server_name lbadmin.traclist.com;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/Traclist/traclist/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }
  
  access_log        /var/log/nginx/traclist/admin1.access.log;
  error_log         /var/log/nginx/traclist/admin1.error.log;


  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    proxy_pass http://web_cluster_admin;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }

}


upstream web_cluster_api {

  least_conn;
  server  app1.traclist.com:8082;
  server  app2.traclist.com:8082;
}

server {
  server_name lbapi.traclist.com;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/Traclist/traclist/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }

  
  access_log        /var/log/nginx/traclist/api1.access.log;
  error_log         /var/log/nginx/traclist/api1.error.log;

  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    proxy_pass http://app2.traclist.com:8082;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }

}

server {
  server_name lbwechat.traclist.com;
  listen 80;
 
  location ~ ^/(img|js|css|fonts)/ {  # |pi||ext|theme
    root                    /opt/Traclist/traclist/static;
    add_header              Cache-Control public;
    #expires                 30d;
  }

  
  access_log        /var/log/nginx/traclist/wechat.access.log;
  error_log         /var/log/nginx/traclist/wechat.error.log;

  location / { try_files $uri @yourapplication; }

  location @yourapplication {
    include uwsgi_params;
    proxy_pass http://app2.traclist.com:8082;
    add_header              'Access-Control-Allow-Origin' '*';
    add_header              'Access-Control-Allow-Credentials' 'true';
    add_header              'Access-Control-Allow-Headers' 'Content-Type,Accept,Keep-Alive,User-Agent,X-Requested-With,Cache-Control';
    add_header              'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
  }

}

