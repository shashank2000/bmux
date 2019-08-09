import rumps
from subprocess import Popen

class StatusBarApp(rumps.App):
    def __init__(self):
        # add an icon by setting icon="filepath of icon"
        super(StatusBarApp, self).__init__("BMUX")
        self.menu = ["Start session", "Load session"]
        self.icon = "icon.png"
        self.tabs_file = "tabs.txt"

    @rumps.clicked("Start session")
    def record_tabs(self, _):
        open(self.tabs_file, "w").close()
        p = Popen(["osascript", "safari_tabs.scpt"])
        print("----Tabs recorded----")

    def get_session_names(self):
        with open(self.tabs_file, "r") as f:
            pass #do something
    session_names = ["foo", "bar"]
    for s in session_names:
        @rumps.clicked("Load session", s)
        def load_session(self, _):
            pass

        # every 30 seconds, let us download all the open pages locally. Each time a tab is closed we delete the local copy of it. This is essentially browser tmux
        # LOOK AT RUMPS timer
if __name__ == "__main__":
    StatusBarApp().run()
