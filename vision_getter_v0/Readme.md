Package vision_getter_v0

Principe:
- crée un noeud vision_getter_node
- démarre une souscription au topic /videofile/videofile_image_view/output

Fonctionnement:
- lancer vision_getter_v0.py
rosrun vision_getter_v0 vision_getter_v0.py
- lancer video_stream_opencv:
poser un fichier /tmp/small.mp4
roslaunch video_stream_opencv video_file.launch
