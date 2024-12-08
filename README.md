# Flanellograf [flanellogrˈaf]

_Flanellograf_ is a tool for making presentations in the Python REPL (it is not a terminal user interface (TUI), at every slide you are in the interactive repl with access to the code from the slide).

This is a quick and dirty WIP prototype and making the slideshow interactive in the REPL involves some serious python hackery. There are ruff edges, beware.

A slide can contain a title, markdown content and Python code. Python code in the slide is ran as you go trough the presentation, meaning that any example in a slide can be further explained using the REPL.

## Installation
The tool will work on Python 3.9 and above, however with the improvements to the REPL in Python 3.13, that version is recomended (especially the multiline editing feature, but built in syntax highlighting is also nice). 

The code is published to PyPI so `pip install flanellograf` should work, it will also install it's only requirement `rich`. 

You could also clone or zip this project and run `pip install .`.

It's prefered to install _Flanellograf_ into a virtual environment regardless of installation method.

If you are presenting some code from your own project just add `flanellograf` as a dev-dependency and check the slides into git. This way the presentation can be part of the documentation of your project. You can use your development tools like linter and formaters, and even test your presentation (mind-blown) giving you a heads up if change break one of your slides.

## Usage

For now flanellograf must be called as a module with a path parameter:
`python -im flanellograf path_to_folder_or_file`

Any file found in path with the glob pattern `**/board_*.py` will be read as a board and listed in the TOC.

See the `examples` directory for how to make a board.

### Navigation
A shorthand name for your board(s) are automatically made (they are listed in the TOC shown at startup). With the example board named `board_example.py` the shorthand becomes `e`.

`~e`
: Refresh current slide (remove anything you have done in the REPL)

`e`
: Next slide

`-e`
: Previous slide

`+e`
: Jump to first slide

`e(n)`
: Jump to slide number n, where n is an integer. (Negative numbers count from the end)


## Inspiration
Inspiration and ideas for making this tool.

- Talks by David Beazley at PyOhio 2016 and PyData Chicago 2016
    - https://www.youtube.com/watch?v=Bm96RqNGbGo
    - https://www.youtube.com/watch?v=j6VSAsKAj98
- ASCII (extended) diagrams
    - https://asciiflow.com/