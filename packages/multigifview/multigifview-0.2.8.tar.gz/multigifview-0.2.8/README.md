MultiGifView
============

MultiGifView is a bare-bones Python program for viewing several .gif files at
once, with their play-back synchronised.

The gifs are opened in two columns.

### Installation

Install with pip

    $ pip install multigifview

or with conda

    $ conda install -c conda-forge multigifview

#### known issues

Installing an unreleased version with pip from the git repo like this

    $ python -m pip install --user https://github.com/johnomotani/multigifview.git

is expected to fail because of a missing man page file. As an alternative,
clone the repo and see ``DEVELOPMENT.md`` for how to install.

### Usage

    $ multigifview movie1.gif movie2.gif movie3.gif ...

Once the window is opened:

* play/pause - space, or click play button in bottom left

* next frame - n, right arrow or seek-forward button in bottom left

* previous frame - p, left arrow or seek-backward button in bottom left

* end - e, down arrow, or skip-forward button in bottom left

* beginning - b, up arrow, or skip-backward button in bottom left

* zoom out - - or zoom-out button at bottom

* zoom in - + or zoom-in button at bottom

* zoom to scale factor - enter number (in %) into box in bottom panel and press
  enter

* quit - q, Ctrl-q, Ctrl-w, Ctrl-x, button in bottom right or close the window

Command line argumens:

``-c, --max-columns <i>`` : use at most ``<i>`` columns for display

``-h, --help`` : print help text

``-n, --no-titles``: turn off titles over each gif

``-v, --version`` : print the version number

``-z, --zoom`` : set the initial zoom level in %

### In Python code

MultiGifView can be used from within Python code.

    >>> from multigifview import show_gifs
    >>> show_gifs("gif1.gif", "gif2.gif")

Any number of gifs can be passed as positional arguments. ``max_columns`` can
be passed as a keyword argument. An argument ``titles=False`` can be passed to
turn off titles above gifs.

Contributing
------------

Contributions are welcome at the [Github
repo](https://github.com/johnomotani/multigifview). For some notes on
developing MultiGifView see [DEVELOPMENT.md](DEVELOPMENT.md).

Acknowledgements
----------------

Contributors: [John Omotani](https://github.com/johnomotani)

#### Thanks

From John Omotani to [Peter Hill](https://github.com/ZedThree) for writing the
gui for [hypnotoad](https://github.com/boutproject/hypnotoad) from which I
learned to make a Qt gui in Python.
