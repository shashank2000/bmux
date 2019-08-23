import rumps
import subprocess

class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__("BMUX")

        self.icon = "images/standard_icon.png"
        self.temp_file = "data/temp_tabs.txt"
        self.tabs_file = "data/tabs.txt"
        self.script_file = "scripts/tabs_script.scpt"

        self.current_session = ""

        self.load_menu = []
        self.delete_menu = []
        self.load_all_sessions()

        self.menu = ["Start session",
                     ("Load session", self.load_menu),
                     ("Delete session", self.delete_menu)]

    def load_all_sessions(self):
        """This method is for initializing the sessions from the init function."""
        session_names = self.get_session_names()
        for name in session_names:
            load_item = rumps.MenuItem(name, callback=self.load_session)
            delete_item = rumps.MenuItem(name, callback=self.delete_session)
            self.load_menu.append(load_item)
            self.delete_menu.append(delete_item)

    def read_sessions(self):
        """Reads sessions from self.tabs_file and returns a dictionary with keys as session
        names and values as a list of URLs
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
        """Writes the passed dictionary into tabs_file.
        """
        with open(self.tabs_file, "w") as f:
            for session_name in sessions:
                urls = sessions[session_name]
                f.write("Name: " + session_name + "\n")
                for url in urls:
                    f.write(url + "\n")
                f.write("\n")

    @rumps.timer(10)
    def update_tabs(self, _):
        """This function makes sure that tabs are up-to-date."""
        if not self.current_session: return
        print("Current session is", self.current_session)
        open(self.temp_file, "w").close()
        subprocess.check_output(["osascript", self.script_file])
        print("----Tabs found----")

        url_list = []
        name = ""
        with open(self.temp_file, "r") as temp_file:
            for line in temp_file.readlines():
                value = line.strip()
                if "missing value" not in value:
                    url_list.append(line.strip())

        sessions = self.read_sessions()
        sessions[self.current_session] = url_list
        self.write_sessions(sessions)
        print("----Tabs recorded----")
        self.update_all_sessions()

    @rumps.clicked("Start session")
    def record_tabs(self, _):
        """Starts a new session, records tabs, and calls update_tabs to refresh the menu to
        reflect the new session.
        """
        response = rumps.Window(
            cancel="fuggetaboutit",
            title="Enter a session name",
            dimensions=(300,20)
        ).run()
        if not response.clicked: return
        session_name = response.text
        sessions = self.read_sessions()
        if not session_name:
            base_string = "session_"
            base_number = 1
            while True:
                session_name = base_string + str(base_number)
                if session_name not in sessions: break
                base_number += 1
        print("Creating session", session_name)
        self.current_session = session_name
        self.update_tabs()

    def end_session(self, _):
        """This method ends any current session that may be running and updates the menu
        accordingly.
        """
        self.current_session = ""
        self.update_all_sessions()

    def get_session_names(self):
        """This method returns all the session names stored in self.tabs_file."""
        session_names = []
        with open(self.tabs_file, "r") as f:
            for line in f.readlines():
                if line.startswith("Name"):
                    session_names.append(" ".join(line.split(" ")[1:]).strip())
        return session_names

    def update_all_sessions(self):
        """This method updates the menu to reflect the current state of self.tabs_file."""
        session_names = self.get_session_names()
        load_menu = rumps.MenuItem("Load session")
        delete_menu = rumps.MenuItem("Delete session")
        for name in session_names:
            if name == self.current_session: continue
            load_item = rumps.MenuItem(name, callback=self.load_session)
            delete_item = rumps.MenuItem(name, callback=self.delete_session)
            load_menu.add(load_item)
            delete_menu.add(delete_item)
        self.menu.clear()
        if self.current_session:
            self.menu.add(rumps.MenuItem(self.current_session))
            self.menu.add(rumps.MenuItem("End session", callback=self.end_session))
        else:
            self.menu.add(rumps.MenuItem("Start session", callback=self.record_tabs))
        self.menu.add(load_menu)
        self.menu.add(delete_menu)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def load_session(self, var):
        """Loads the session name passed in as var by loading it from self.tabs.txt, then
        updates menu to reflect this.
        """
        session_data = self.read_sessions()
        websites = session_data[var.title]
        subprocess.check_output(["open -n"] + websites)
        self.current_session = var.title
        self.update_all_sessions()

    def delete_session(self, var):
        """Deletes the session passed in as var and makes sure that self.current_session is
        changed to an empty string if it is the session that was deleted.
        """
        session_data = self.read_sessions()
        new_session_data = {}
        for session in session_data:
            if session != var.title:
                new_session_data[session] = session_data[session]
        self.write_sessions(new_session_data)
        if self.current_session == var.title:
            self.current_session = ""
        self.update_all_sessions()

if __name__ == "__main__":
    StatusBarApp().run()
