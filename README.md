# Descent Dice

This is a little tool that will dynamically plot dice probability distributions for
<a href="https://boardgamegeek.com/boardgame/104162/descent-journeys-dark-second-edition">
Descent: Journeys in the Dark (Second Edition)</a>.

<p align="center">
	<img src="https://raw.githubusercontent.com/theanine/descent-dice/master/img/console.png"
			width="200">
	<img src="https://raw.githubusercontent.com/theanine/descent-dice/master/img/graph.png"
			width="500">
</p>


## Usage

Install `python3` if you don't have it:

```sh
$ sudo apt-get install python3.6
```

Next install some needed packages:

```sh
$ pip3 install matplotlib IPython joblib
$ sudo apt-get install python3-tk
```

And run (interactive mode):

```sh
$ ./dice
```

Or pass CLI args:

```sh
$ ./dice --blue --red --white=2
```
