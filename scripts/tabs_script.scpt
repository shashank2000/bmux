set myText to ""
set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "../data/temp_tabs.txt" as POSIX file) with write permission

if application "Safari" is running then
  tell application "Safari"
    if the number of windows is greater than 0 then
      set myTabs to every tab of window 1
      repeat with aTab in myTabs
        set tabURL to URL of aTab & "\n"
        set myText to myText & tabURL
      end repeat
    end if
  end tell
end if

if application "Google Chrome" is running then
  tell application "Google Chrome"
    if the number of windows is greater than 0 then
      set myTabs to every tab of window 1
      repeat with aTab in myTabs
        set tabURL to URL of aTab & "\n"
        set myText to myText & tabURL
      end repeat
    end if
  end tell
end if

write myText to myFile
close access myFile
