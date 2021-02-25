Package vision_getter_v1

Principe:
- crée un noeud listener
- démarre une souscription au topic custom_chatter
- le talker émet sur le noeud custom_chatter

Fonctionnement:
- lancer listener.py
rosrun vision_getter_v1 listener.py
- lancer talker02.py:
rosrun vision_getter_v1 talker02.py
