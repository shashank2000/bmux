import rumps
from subprocess import Popen

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        # add an icon by setting icon="filepath of icon"
        super(AwesomeStatusBarApp, self).__init__("Awesome App")
        self.menu = ["Start bmux session", "Run an apple script", "Say hi"]

    @rumps.clicked("Run an apple script")
    def prefs(self, _):
        script= '''
        tell Application "Safari" set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "tabs.txt" as POSIX file) with write permission 
        set windowNumber to 1 
        set myTabs to every tab of window windowNumber
        repeat the number of windows times
    write "----- Window Number " & windowNumber & " -----\n\n" to myFile
    set tabNumber to 0
    repeat with aTab in myTabs

      set tabTitle to "Name: " & name of aTab & "\n"
      write tabTitle to myFile
      set tabURL to "URL: " & URL of aTab & "\n\n"
      write tabURL to myFile
      set tabNumber to tabNumber + 1

    end repeat

    write "Window Number: " & windowNumber & " Number of tabs: " & tabNumber & "\n\n" to myFile
    set windowNumber to windowNumber + 1
    end repeat
	close access myFile

    end tell'''

        chrome_script = '''
        tell Application "Chrome" set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "tabs.txt" as POSIX file) with append 
        set windowNumber to 1 
            set myTabs to every tab of window windowNumber
        repeat the number of windows times
        write "----- Window Number " & windowNumber & " -----\n\n" to myFile
        set tabNumber to 0
        repeat with aTab in myTabs

        set tabTitle to "Name: " & name of aTab & "\n"
         write tabTitle to myFile
         set tabURL to "URL: " & URL of aTab & "\n\n"
         write tabURL to myFile
         set tabNumber to tabNumber + 1

          end repeat

            write "Window Number: " & windowNumber & " Number of tabs: " & tabNumber & "\n\n" to myFile
            set windowNumber to windowNumber + 1
        end repeat
            close access myFile

        end tell'''
        p = Popen(['osascript', '-e', chrome_script])

        # add an icon 
    @rumps.clicked("Start session")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

        # every 30 seconds, let us download all the open pages locally. Each time a tab is closed we delete the local copy of it. This is essentially browser tmux
if __name__ == "__main__":
    AwesomeStatusBarApp().run()
