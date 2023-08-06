# enocean_webthing
A web connected enocean gateway. This project provides a [webthing API](https://iot.mozilla.org/wot/) to an enocean gateway such as the  [EnOcean USB 300 USB-Gateway](https://www.enocean.com/de/produkt/usb-300-500u-400j/)

The enocean_webthing package exposes a http webthing endpoint supporting enocean devices. 

E.g.
```
# webthing has been started on host 192.168.0.23

curl http://192.168.1.198:9090/0/properties

{
   "eep_id":"F6:10:00",
   "enocean_id":"81:00:F0:4E",
   "state":3
}
```
Currently, the [devices](https://www.enocean-alliance.org/wp-content/uploads/2017/05/EnOcean_Equipment_Profiles_EEP_v2.6.7_public.pdf) listed below are supported
* Window Handle such as [HOPPE Window Handle ConnectHome](https://www.hoppe.com/in-en/window-handles/hoppe-innovations-window-handles/ehandle-connecthome-for-windows/) (EEP ID: F6:10:00)

To install this software you may use the [PIP](https://realpython.com/what-is-pip/) package manager such as shown below

**PIP approach**
```
sudo pip install enocean_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo enocean --command listen --port 9090 --path /dev/ttyUSB-enocean --devices 'Office/F6:10:00/81:00:F0:4E, Patiodoor/F6:10:00/01:9A:CC:06'
```
Here, the webthing API will be bound to the local port 9090 by using the USB-Gateway /dev/ttyUSB-enocean. 
To list the devices to be supported a comma-separated list is used with the syntax {Device name}/{EEP ID}/{ENOCEAN ID}    

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit.
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary.
```
sudo enocean --command register --port 9090 --path /dev/ttyUSB-enocean --devices 'Office/F6:10:00/81:00:F0:4E, Patiodoor/F6:10:00/01:9A:CC:06'
```  