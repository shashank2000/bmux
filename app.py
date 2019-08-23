import rumps
import subprocess
import time

# could use this if rumps timer screws up: https://pypi.org/project/schedule/
class StatusBarApp(rumps.App):
    def __init__(self):
        super(StatusBarApp, self).__init__("BMUX")

        self.icon = "icon.png"
        self.temp_file = "temp_tabs.txt"
        self.tabs_file = "tabs.txt"
        self.script_file = "safari_tabs.scpt"

        self.current_session = ""
        self.browser = "Safari"

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
        """this function is called every time we load a session or start a session, or on the current session"""
        if self.current_session:
            print("Current session is", self.current_session)
        if self.current_session:
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

            url_list = []
            for tab_name in tabs:
                url = tabs[tab_name]
                url_list.append(url)
            sessions = self.read_sessions()
            print(sessions)
            sessions[self.current_session] = url_list
            self.write_sessions(sessions)
            


    @rumps.clicked("Start session")
    def record_tabs(self, _):
        '''starts a new session, records tabs, and calls update_all_sessions to refresh the menu to reflect this'''
        response = rumps.Window(
            default_text="my cool session",
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
                    value = " ".join(line.split(" ")[1:]).strip()
                    if value != "missing value":
                        tabs[name] = value
                    else:
                        del tabs[name]

        sessions = self.read_sessions()
        print(sessions)
        url_list = []
        for tab_name in tabs:
            url = tabs[tab_name]
            url_list.append(url)

        # needs to be fixed
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
        self.current_session = session_name
        self.update_all_sessions()
        


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

    def load_session(self, var):
        '''loads a session from the text file, and updates menu to reflect this'''
        session_data = self.read_sessions()
        websites = session_data[var.title]
        subprocess.check_output(["open"] + websites)
        self.current_session = var.title
        load_all_sessions()

    def delete_session(self, var):
        session_data = self.read_sessions()
        new_session_data = {}
        for session in session_data:
            if session != var.title:
                new_session_data[session] = session_data[session]
        self.write_sessions(new_session_data)
        self.update_all_sessions()

if __name__ == "__main__":
    StatusBarApp().run()
