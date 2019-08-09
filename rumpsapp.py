import rumps
from subprocess import Popen

class StatusBarApp(rumps.App):
    def __init__(self):
        # add an icon by setting icon="filepath of icon"
        super(StatusBarApp, self).__init__("BMUX")
        self.menu = ["Start bmux session"]

    @rumps.clicked("Start bmux session")
    def prefs(self, _):
        with open("safari_tabs.scpt", "r") as f:
            script = f.read().replace("\n", "")
        osa_file = "safari_tabs.scpt"
        p = Popen(["osascript", osa_file])
        print("----Tabs recorded----")

    @rumps.clicked("Notification")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

        # every 30 seconds, let us download all the open pages locally. Each time a tab is closed we delete the local copy of it. This is essentially browser tmux
if __name__ == "__main__":
    StatusBarApp().run()
