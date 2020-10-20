echo "Apply styling"
echo "copying $CP_THEME_HOME/style content to $CP_HOME/catprez/view/style"
cp $CP_THEME_HOME/style/* $CP_HOME/catprez/view/style

echo "Apply templates"
echo "copying $CP_THEME_HOME/templates content to $CP_HOME/catprez/view/templates"
cp $CP_THEME_HOME/templates/* $CP_HOME/catprez/view/templates

echo "Apply model extensions"
echo "copying $CP_THEME_HOME/model content to $CP_HOME/catprez/model"
cp $CP_THEME_HOME/model/* $CP_HOME/catprez/model

echo "Apply config"
echo "replace $CP_HOME/catprez/config.py with $CP_THEME_HOME/config.py"
cp $CP_THEME_HOME/config.py $CP_HOME/catprez/config.py

echo "customisation done"
