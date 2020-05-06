# Inky Annunicator

Takes data from the [annunciator API](https://dm-devci-annunciator-services.azurewebsites.net/index.html), in order to display it on an [Inky pHAT](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811).

## Crontab

To run the script in the background at boot add the following to `crontab`

`@reboot /usr/bin/python3 /home/pi/inky-annunciator/script.py &`

And then rerun the script every minute to catch the new messages:

`* * * * * /usr/bin/python3 /home/pi/inky-annunciator/script.py`
