# RPi TV Noticeboard

### About

This project is a fork of the django-photologue example project that can be found [here](https://github.com/jdriscoll/django-photologue).

### Usage

```
<VirtualHost *:80>
    ServerName www.noticeboard.wncc-iitb.org
    ServerAlias noticeboard.wncc-iitb.org
    #DocumentRoot /var/www/notceboard.wncc-iitb.org/public_html
    ErrorLog /var/www/noticeboard.wncc-iitb.org/error.log
    CustomLog /var/www/noticeboard.wncc-iitb.org/requests.log combined

    Alias /static /var/www/noticeboard.wncc-iitb.org/rpi_server/static

    <Directory /var/www/noticeboard.wncc-iitb.org/rpi_server/static>
        Require all granted
    </Directory>

    <Directory /var/www/noticeboard.wncc-iitb.org/rpi_server>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>


    WSGIDaemonProcess wncc_noticeboard python-path=/var/www/noticeboard.wncc-iitb.org/rpi_server:/var/www/noticeboard.wncc-iitb.org/rpi_server/rpi_serverenv/lib/python2.7/site-packages
    WSGIProcessGroup wncc_noticeboard
    WSGIScriptAlias / /var/www/noticeboard.wncc-iitb.org/rpi_server/rpi_server/wsgi.py

</VirtualHost>
```