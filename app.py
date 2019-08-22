import rumps
import subprocess

class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__("BMUX")

        self.icon = "icon.png"
        self.temp_file = "temp_tabs.txt"
        self.tabs_file = "tabs.txt"
        self.script_file = "safari_tabs.scpt"

        self.load_menu = []
        self.delete_menu = []
        self.load_all_sessions()
        self.menu = ["Start session",
                     ("Load session", self.load_menu),
                     ("Delete session", self.delete_menu)]

    def read_sessions(self):
        """Reads sessions from tabs_file. Returns a dictionary with keys as session names
        and values as a list of URLs
        """
        sessions = {}
        session_name = ""
        urls = []
        with open(self.tabs_file, "r") as f:
            for line in f.readlines():
                if line.startswith("Name") or line.isspace():
                    if session_name:
                        sessions[session_name] = urls
                    session_name = " ".join(line.split(" ")[1:]).strip()
                    urls = []
                else:
                    urls.append(line.strip())
        return sessions

    def write_sessions(self, sessions):
        """Writes the passed dictionary into tabs_file
        """
        #open(self.tabs_file, "w").close()
        with open(self.tabs_file, "w") as f:
            for session_name in sessions:
                urls = sessions[session_name]
                f.write("Name: " + session_name + "\n")
                for url in urls:
                    f.write(url + "\n")
                f.write("\n")

    @rumps.clicked("Start session")
    #@rumps.timer(60) # run record_tabs every 60 seconds
    def record_tabs(self, _):
        response = rumps.Window(
            cancel="Cancel",
            title="Enter a session name",
            dimensions=(300,20)
        ).run()
        if not response.clicked: return
        session_name = response.text

        open(self.temp_file, "w").close()
        subprocess.check_output(["osascript", self.script_file])
        print("----Tabs found----")

        tabs = {}
        name = ""
        with open(self.temp_file, "r") as temp_file:
            for line in temp_file.readlines():
                if line.startswith("Name"):
                    name = " ".join(line.split(" ")[1:]).strip()
                elif line.startswith("URL"):
                    tabs[name] = " ".join(line.split(" ")[1:]).strip()

        sessions = self.read_sessions()
        print(sessions)
        url_list = []
        for tab_name in tabs:
            url = tabs[tab_name]
            url_list.append(url)
        if not session_name:
            base_string = "session_"
            base_number = 1
            while True:
                session_name = base_string + str(base_number)
                if session_name not in sessions: break
                base_number += 1
        sessions[session_name] = url_list

        self.write_sessions(sessions)
        print("----Tabs recorded----")

    def get_session_names(self, tabs_file):
        session_names = []
        with open(tabs_file, "r") as f:
            for line in f.readlines():
                if line.startswith("Name"):
                    session_names.append(" ".join(line.split(" ")[1:]).strip())
        return session_names

    #session_names = get_session_names("tabs.txt") # Hack solution

    def load_all_sessions(self):
        session_names = self.get_session_names(self.tabs_file)
        for name in session_names:
            load_item = rumps.MenuItem(name, callback=self.load_session)
            delete_item = rumps.MenuItem(name, callback=self.delete_session)
            self.load_menu.append(load_item)
            self.delete_menu.append(delete_item)

    def load_session(self, var):
        session_data = self.read_sessions()
        websites = session_data[var.title]
        subprocess.check_output(["open"] + websites)
        #rumps.alert("load_session was triggered, with session name " + session_name)

    def delete_session(self, var):
        session_data = self.read_sessions()
        new_session_data = {}
        for session in session_data:
            if session != var.title:
                new_session_data[session] = session_data[session]
        self.write_sessions(new_session_data)

if __name__ == "__main__":
    StatusBarApp().run()
