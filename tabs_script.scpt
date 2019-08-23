set myText to ""
set myFile to open for access file (POSIX path of ((path to me as text) & "::") & "temp_tabs.txt" as POSIX file) with write permission

if application "Safari" is running then
	tell application "Safari"
		set myTabs to every tab of window 1
		repeat with aTab in myTabs
			set tabURL to URL of aTab & "
"
			set myText to myText & tabURL
		end repeat
	end tell
end if

if application "Google Chrome" is running then
	tell application "Google Chrome"
		set myTabs to every tab of window 1
		repeat with aTab in myTabs
			set tabURL to URL of aTab & "
"
			set myText to myText & tabURL
		end repeat
	end tell
end if

write myText to myFile
close access myFile
