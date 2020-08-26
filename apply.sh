# apply new config
echo "update $CP_THEME_HOME/config.py with data dir ($CP_THEME_HOME/data)"
CP_DATA_DIR=$CP_THEME_HOME/data
sed -i "s#CP_DATA_DIR#$CP_DATA_DIR#" $CP_THEME_HOME/config.py
echo "copying $CP_THEME_HOME/config.py to $CP_HOME/catprez/config.py"
cp $CP_THEME_HOME/config.py $CP_HOME/catprez/config.py

# copy all style content to CP
echo "copying $CP_THEME_HOME/style content to $CP_HOME/catprez/view/style"
cp $CP_THEME_HOME/style/* $CP_HOME/catprez/view/style

# overwrite templates
echo "copying $CP_THEME_HOME/templates content to $CP_HOME/catprez/view/templates"
cp $CP_THEME_HOME/templates/* $CP_HOME/catprez/view/templates

## append paths to CP routes, removing running locally commands
#echo "adding new routes to $CP_HOME/catprez/app.py"
## truncate app.py
#sed -i -n '/# run the Flask app/q;p' $CP_HOME/catprez/app.py
## add new routes
#cat $CP_THEME_HOME/routes.txt >> $CP_HOME/catprez/app.py

echo "customisation done"
