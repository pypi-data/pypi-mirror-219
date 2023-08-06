# Topoo

A [textual](https://textual.textualize.io) based application to present your
markdown-based slides inside the terminal. Great if you plan on sharing your
terminal with your audience since you can easily switch between your
tabs/windows/panes. Not so great if your presentation includes anything
graphically.

Take a look at demo presentation (`potoo example_presentation.md`) or even this
file itself (`pocoo README.md`). Alternatively you can take a look at the
(initial) export capabilities by browsing the `assets/` directory.

## Features

- Slide counter at the bottom
- Custom centered footer content via `-f/--static-footer`

### Shortcuts

Note: Not all shortcuts are shown inside the help footer to keep it as clean as
possible.

- `p`/`k`/`backspace`/`left`: Previous slide
- `n`/`j`/`space`/`right`: Next slide
- `?`: Toggle the help bar at the bottom. It's the default
  [Footer](https://textual.textualize.io/widgets/footer/) of textual which means
  that you also click the buttons.
- `.`: "Pause" the presentation by blanking the screen.
- `d`: Toggle between light and dark mode.
- `o`: Open an overview of all slides with the ability to jump quickly to any
  one of them
- `ctrl+d`: Scroll down
- `ctrl+u`: Scroll up

## Usage

### Metadata/Frontmatter

We support YAML based "frontmatter" (YAML between two `---` lines) at the very
beginning of the file. The following (string) keys are recognized and will be
used to build the first slide ("Title slide"):

- `title` (recommended): Also shown in the bottom left corner and at the top of
  all exports
- `subtitle` (optional): Also shown on the title slide
- `author` and `date`: Included on the title slide

The title(s) are also used to set the terminal title while the presentation is
running.

## FAQ

### How can I change the font size?

Increase your terminal font size accordingly.

### What's up with the name?

Since the textual project, apparently, started naming their textual based
applications after bird species I searched for one with large eyes, since you
usually need to zoom in on your terminal to get to a usable font size **and**
whose name wasn't already taken on PyPI. _Potoo_ seemed perfect since, according
to Wikipedia, they "are a group of birds related to the nightjars and
_frogmouths_" and guess what the
[textual based markdown viewer](https://github.com/Textualize/frogmouth) is
called.
