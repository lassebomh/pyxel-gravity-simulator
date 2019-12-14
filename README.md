# pyxel-gravity-simulator
This project is a sandbox minigame that simulates gravity. It was made purely for fun in my spare time, so i didn't bother to optimize it. The game uses [gradients](https://en.wikipedia.org/wiki/Gradient) (partial derivatives) to calculate the forces, and [the python module pyxel](https://pypi.org/project/pyxel/) for GUI.

### Pyxel
I choose pyxel because of its simplicity, but I do not recommend it's use if you're expecting to expand your project beyond a basic concept pierce. You quickly run into limitations such as the limit to only use 16 different colors, as well as the maximum resolution of 255 x 255 pixels. If i was ever to redo the project, i would most likely build it with [pyglet](http://pyglet.org/) - another very powerful and pythonic API for videogames and the like.  

![](https://media.giphy.com/media/JRDog1OxB7g2jdI8Rv/giphy.gif)

# Features
#### Resize planets  
![](https://media.giphy.com/media/JoPrWaF4IymEc9giz9/giphy.gif)

#### Predict the future!  
![](https://media.giphy.com/media/MBfxqlYapwfZoapIpn/giphy.gif)

#### Planets can collide  
![](https://media.giphy.com/media/j2SqilfUPiXoesvATj/giphy.gif)

# How to use

 1. Install the pyxel module  
 ```$ pip install pyxel```

 2. Download the script  
 ```$ git clone https://github.com/lassebomh/pyxel-gravity-simulator/```  
 ```$ cd pyxel-gravity-simulator/```

 3. Run it  
 ```$ python main.py```
