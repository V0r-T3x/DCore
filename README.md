# DCore
 Display Manager multiple screens, screen types and multiple frames input  
 **Experimental work**

# Installation steps
_Need internet connection_
- Go in the home folder:
```
cd /home/pi
```
- Clone this github repo:
```
git clone https://github.com/V0r-T3x/DCore.git DCore-repo
```
- Go inside the repo scripts folder:
```
cd /home/pi/DCore-repo/scripts/
```
- Make the scripts executable and run the install script.
  - This will create the python venv in `/home/pi/DCore`
```
chmod +x install.sh
./install.sh
```
- Activate the python venv.
```
source /home/pi/DCore/bin/act*
```
- Configure DCore with the rigth screens and inputs.
```
nano /home/pi/DCore/lib/python3.11/site-packages/DCore/config.yaml
```
- Configuration file exemple:
```
screens:
  screen1:
    name: "displayhatmini" # "waveshare_3.5_clone" or "gamepi_1.5_lcd" (actual compatible screens)
    spi_port: 0
    default_input: input1

frame_inputs:
  input1:
    type: "retrieved" # or "received"
    name: "pwnagotchi"
    path: "/var/tmp/pwnagotchi/pwnagotchi.png"
```
- Starting DCore.
```
python3 -m DCore
```
