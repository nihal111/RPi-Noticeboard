# RPi-Noticeboard

### About
This project consists of two parts.
- **RPi**: Contains the code that runs on the RPi, to fetch and display the images.
- **Server**: Contains the django project that serves as a backend to allow addition of photos to different galleries. The RPi fetches the photos from this server.

### Usage

To run the RPi TV Noticeboard, you need to-
1. Host the Django application on a server and configure it as described in the readme inside [server folder](server).
2. Set up the scripts on an RPi as described in the readme inside [rpi](rpi).
