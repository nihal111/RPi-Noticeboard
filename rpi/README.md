# RPi TV Noticeboard

### About

The contents of this folder are to be copied to the RPi. There are 3 essential parts-
- **fetch.py**: A Python script that runs in the background and periodically fetches images from the server. We set up a cron job for this.
- **gui.py**: The main script that runs on boot and occupies the foreground. This displays the images on the TV.
- **config.json**: Helps you define the configuration for how you want the images to appear on the TV.

### Setup

1. Install a standard Raspbian OS on the RPi.
2. Configure the RPi to connect to internet. If it is an RPi-3, connect using wifi. Follow the [official docs](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) to learn how to connect through wifi. To connect to IITB-Wireless, use the wpa_supplicant.conf specified [here](https://gist.github.com/nihal111/56a0317fb61596cd17f2bb080591ba40). For RPi 2 or below, connect using an external wifi module or ethernet.
3. SSH into the RPi.
4. On the RPi, download the `rpi` folder. //Insert command
5. On the RPi, execute `sudo apt-get install python-tk python-imaging python-imaging-tk x11-xserver-utils`
6. On the RPi, execute `sudo crontab -e`. It might prompt you to choose a text editor. (Choose nano if you don't know what to do.) Add the following line at the bottom of the file- `* * * * * (cd /home/pi/rpi/; python fetch.py) >> /home/pi/rpi/TV_log.txt 2>&1`. This would run our fetch script every minute and save all output in the TV_log file created inside `~/rpi`. 
7. On the RPi, cd into the `rpi` folder and execute `chmod 755 launcher.sh`.
8. On the RPi, execute `sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart`. Add the following line to the bottom- `@sh /home/pi/rpi/launcher.sh`.
9. Disable standby screen blanking. Execute `sudo nano ~/.config/lxsession/LXDE-pi/autostart` and add the following-
```
@xset s 0 0
@xset s noblank
@xset s noexpose
@xset dpms 0 0 0
```
Ctrl + X, Y and Enter. Hit `sudo reboot`