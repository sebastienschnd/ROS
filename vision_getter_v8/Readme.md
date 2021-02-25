Package vision_getter_v8

Principe:
- illustration du talker/listener pour l'envoi d'un flux d'images contenues dans un répertoire
- application de YOLO OpenCV sur les images
- publication des informations YOLO

Fonctionnement:
- disposer des images sous /tmp/images/*.jpg
- lancer le listener depuis son répertoire
python vision_getter.py
- lancer le talker depuis son répertoire
python vision_device.py
