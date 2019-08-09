tell application "Safari"

  set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "temp_tabs.txt" as POSIX file) with write permission
  set windowNumber to 1
  set myTabs to every tab of window windowNumber
  repeat the number of windows times
    write "Window\n" to myFile
    repeat with aTab in myTabs

      set tabTitle to "Name: " & name of aTab & "\n"
      write tabTitle to myFile
      set tabURL to "URL: " & URL of aTab & "\n"
      write tabURL to myFile

    end repeat
  end repeat
	close access myFile

end tell
