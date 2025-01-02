# DCore
 Display Manager multiple screens, screen types and multiple frames input  
 **Experimental work**

# Installation steps
- copy create_venv.py in /home/pi
```
cd /home/pi
python3 create_venv.py DCore
source /home/pi/DCore/bin/act*
```
- copy DCore files in /home/pi/DCore/lib/python3.11/site-packages/DCore
```
cd /home/pi/DCore/lib/python3.11/site-packages/DCore
chmod +x setup.sh
```
- need internet connection to download packages and requirements
```
./setup.sh
```
- configure DCore with the rigth screens and inputs
```
python3 -m DCore
```
