import rumps
from subprocess import Popen

class StatusBarApp(rumps.App):
    def __init__(self):
        # add an icon by setting icon="filepath of icon"
        super(StatusBarApp, self).__init__("BMUX")
        self.menu = ["Start session", "Load session"]
        self.icon = "icon.png"
        self.temp_file = "temp_tabs.txt"
        self.tabs_file = "tabs.txt"
        self.script_file = "safari_tabs.scpt"

    @rumps.clicked("Start session")
    def record_tabs(self, _):
        response = rumps.Window(
            cancel="Cancel",
            title="Enter a session name",
            dimensions=(300,20)
        ).run()
        if not response.clicked: return
        session_name = response.text

        open(self.temp_file, "w").close()
        p = Popen(["osascript", self.script_file])
        print("----Tabs recorded----")

        tabs = {}
        with open(self.temp_file, "r") as temp_file:
            line = temp_file.readline()
            name = ""
            if line.startswith("Name"):
                name = line.split(" ")[1]
            elif line.startswith("URL"):
                tabs[name] = line.split(" ")[1]

        with open(self.tabs_file, "w") as data_file:
            line = data_file.readline()


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
