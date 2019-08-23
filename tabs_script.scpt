set myText to ""
set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "temp_tabs.txt" as POSIX file) with write permission

set appName to "Safari"
if application appName is running then
  tell application appName
    set myTabs to every tab of window 1
    repeat with aTab in myTabs
      set tabURL to URL of aTab & "\n"
      set myText to myText & tabURL
    end repeat
  end tell
end if

set appName to "Chrome"
if application appName is running then
  tell application appName
    set myTabs to every tab of window 1
    repeat with aTab in myTabs
      set tabURL to URL of aTab & "\n"
      set myText to myText & tabURL
    end repeat
  end tell
end if

write myText to myFile
close access myFile
