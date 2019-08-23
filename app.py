import rumps
import subprocess
import time

class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__("BMUX")

        self.icon = "icon.png"
        self.temp_file = "temp_tabs.txt"
        self.tabs_file = "tabs.txt"
        self.script_file = "tabs_script.scpt"

        self.current_session = ""

        self.load_menu = []
        self.delete_menu = []
        self.load_all_sessions()
        self.update_tabs(None)
        self.menu = ["Start session",
                     ("Load session", self.load_menu),
                     ("Delete session", self.delete_menu)]
        self.quit_button = "Quit"

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
        with open(self.tabs_file, "w") as f:
            for session_name in sessions:
                urls = sessions[session_name]
                f.write("Name: " + session_name + "\n")
                for url in urls:
                    f.write(url + "\n")
                f.write("\n")

    @rumps.timer(10)
    def update_tabs(self, _):
        """This function should be called every time we load a session or start a session, or on the current session."""
        if not self.current_session: return
        print("Current session is", self.current_session)
        open(self.temp_file, "w").close()
        subprocess.check_output(["osascript", self.script_file])
        print("----Tabs found----")

        url_list = []
        name = ""
        with open(self.temp_file, "r") as temp_file:
            for line in temp_file.readlines():
                url_list.append(line.strip())

        sessions = self.read_sessions()
        sessions[self.current_session] = url_list
        self.write_sessions(sessions)
        print("----Tabs recorded----")

    @rumps.clicked("Start session")
    def record_tabs(self, _):
        """Starts a new session, records tabs, and calls update_tabs to refresh the menu to reflect this"""
        response = rumps.Window(
            default_text="my cool session",
            cancel="Cancel",
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

    def get_session_names(self, tabs_file):
        session_names = []
        with open(tabs_file, "r") as f:
            for line in f.readlines():
                if line.startswith("Name"):
                    session_names.append(" ".join(line.split(" ")[1:]).strip())
        return session_names

    def load_all_sessions(self):
        session_names = self.get_session_names(self.tabs_file)
        for name in session_names:
            load_item = rumps.MenuItem(name, callback=self.load_session)
            delete_item = rumps.MenuItem(name, callback=self.delete_session)
            self.load_menu.append(load_item)
            self.delete_menu.append(delete_item)

    def update_all_sessions(self):
        print("update all sessions was called")
        session_names = self.get_session_names(self.tabs_file)
        load_menu = rumps.MenuItem("Load session")
        delete_menu = rumps.MenuItem("Delete session")
        for name in session_names:
            load_item = rumps.MenuItem(name, callback=self.load_session)
            delete_item = rumps.MenuItem(name, callback=self.delete_session)
            load_menu.add(load_item)
            delete_menu.add(delete_item)
        self.menu.clear()
        self.menu.add(rumps.MenuItem("Start session", callback=self.record_tabs))
        self.menu.add(load_menu)
        self.menu.add(delete_menu)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))
        if self.current_session:
                self.menu.add(rumps.MenuItem(self.current_session))
                print("added current_session to menu")

    def load_session(self, var):
        """loads a session from the text file, and updates menu to reflect this"""
        session_data = self.read_sessions()
        websites = session_data[var.title]
        subprocess.check_output(["open"] + websites)
        self.current_session = var.title
        print
        self.update_all_sessions()

    def delete_session(self, var):
        """deletes session, and makes sure the current session is changed to null if it is the session that was deleted"""
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
