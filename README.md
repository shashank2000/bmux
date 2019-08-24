# bmux

_bmux_ is a simple MacOS toolbar widget that lets one manage and persist browser sessions. This is useful for managing multiple browser windows (i.e. for working on different projects).

_bmux_ on the toolbar (leftmost icon):

![bmux icon is on the left](https://raw.githubusercontent.com/shashank2000/bmux/master/images/screenshot.png)

_bmux_ in action:

![bmux in action](https://raw.githubusercontent.com/shashank2000/bmux/master/images/screenshot-2.png)

## Intro
Have you ever wanted to save browser windows over time but didn't want to clutter your desktop? _bmux_ is a tool that lets you create browser environments to save the tabs you have open.

The name _bmux_ is inspired by _tmux_, which is a **t**erminal **mu**ltiple**x**er tool. _bmux_ is accordingly a **b**rowser **mu**ltiple**x**er took.

## Usage
Using _bmux_ is very straightforward. There are three main functions: `Start session`, `Load session`, and `Delete session`.
- `Start session` lets you name a new session. Every 10 seconds, the app will read the URLs that are open in Chrome and Safari and will save them. If your computer shuts down, the session will persist.
- `Load session` lets you load a previously-created session. BMUX will launch a new window with the tabs saved in the session.
- `Delete session` lets you delete a session.

## Download
Download the **v1.0-alpha** release of _bmux_ [here](https://github.com/shashank2000/bmux/releases/download/v1.0-alpha/bmux.zip).

Please let us know if you have any feedback by posting an issue.

## Credits
Developed by [Lucas Pauker](https://github.com/lucaspauker) and [Shashank Rammoorthy](https://github.com/shashank2000)
