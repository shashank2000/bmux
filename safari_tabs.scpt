

tell application "Safari"
	
	set myFile to open for access file "Macintosh HD:Users:shashankrammoorthy:dumbprojects:bmux:safaritabs" with write permission
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

end tell
