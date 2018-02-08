# RPi TV Noticeboard

### About

This project is based on the [django-photologue example project](https://github.com/jdriscoll/django-photologue) with a few modifications.

### Usage

1. Clone this repository inside a folder on the server.
2. Configure a virtual host to get it up and running. A guide like [this](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04) (Ubuntu) or [this](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7) (CentOS) might be handy.
3. The repository is initialised with a few galleries, which should be visible if everything is set up properly.
4. To reset the database, run `python manage.py flush` inside the `server` directory. You should create a superuser after this step using `python manage.py createsuperuser`
5. Execute `sudo crontab -e` and add the following to it `0 0 * * * source /path/to/server/rpi_serverenv/bin/activate && python /path/to/server/manage.py cleanup >> /path/to/server/cronjob.log`. This would cleanup expired photos every midnight.


### Add photos
1. To add photos, login to the admin portal- `https://noticeboard.wncc-iitb.org/admin` (Replace `noticeboard.wncc-iitb.org` with your domain)
2. Head over to photos. Browse and find a photo, choose a title, caption (optional) and set an expiry date.
Note: The expiry date is the date after which the photo will be automatically removed.
3. Head over to the gallery you want to add the photo to, and select the photo by searching for the title you chose in step 2.
4. Save and exit, the photo should now be available. If you face an error while saving, it might be because you've exceeded the MAX_LIMIT defined per gallery. A gallery can only contain MAX_LIMIT number of photos to prevent overuse.


### Fetch List

The list of all galleries and the photos it contains can be found by performing a get request at-  
`https://noticeboard.wncc-iitb.org/list?from=hostel9`
(Replace `noticeboard.wncc-iitb.org` with your domain)

The `from` parameter describes where the request is being made from. By default from is set to `generic`.
Adding a `from` parameter allows access to private galleries that have title starting with `from`.
In the example above the list produced would contain all public galleries and the Hostel9 private gallery as well.
