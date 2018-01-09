
SET INPUT_FILE_NAME_1="uiUserInfo_modified_2.ui"
SET OUTPUT_FILE_NAME_1="ui_user_info_modified.py"
call pyuic4 %INPUT_FILE_NAME_1% -o %OUTPUT_FILE_NAME_1%

SET INPUT_FILE_NAME_2="ui_About.ui"
SET OUTPUT_FILE_NAME_2="ui_about.py"
call pyuic4 %INPUT_FILE_NAME_2% -o %OUTPUT_FILE_NAME_2%

SET INPUT_FILE_NAME_3="ui_AddUser_modified.ui"
SET OUTPUT_FILE_NAME_3="ui_add_user_modified.py"
call pyuic4 %INPUT_FILE_NAME_3% -o %OUTPUT_FILE_NAME_3%

SET INPUT_FILE_NAME_4="ui_RemoveUser.ui"
SET OUTPUT_FILE_NAME_4="ui_remove_user.py"
call pyuic4 %INPUT_FILE_NAME_4% -o %OUTPUT_FILE_NAME_4%

SET INPUT_FILE_NAME_5="uiApplicationWindow.ui"
SET OUTPUT_FILE_NAME_5="ui_application_window.py"
call pyuic4 %INPUT_FILE_NAME_5% -o %OUTPUT_FILE_NAME_5%

SET INPUT_FILE_NAME_6="ui_WelcomeDialog.ui"
SET OUTPUT_FILE_NAME_6="ui_welcome_dialog.py"
call pyuic4 %INPUT_FILE_NAME_6% -o %OUTPUT_FILE_NAME_6%

SET INPUT_FILE_NAME_6="ui_ProxyConnection.ui"
SET OUTPUT_FILE_NAME_6="ui_proxy_connection.py"
call pyuic4 %INPUT_FILE_NAME_6% -o %OUTPUT_FILE_NAME_6%

REM call pyinstaller.exe -F --onefile --windowed --icon=app.ico --version-file=version.txt application.py