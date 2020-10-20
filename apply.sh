echo "Apply styling"
echo "copying $CP_THEME_HOME/style content to $CP_HOME/catprez/view/style"
cp $CP_THEME_HOME/style/* $CP_HOME/catprez/view/style

echo "Apply templates"
echo "copying $CP_THEME_HOME/templates content to $CP_HOME/catprez/view/templates"
cp $CP_THEME_HOME/templates/* $CP_HOME/catprez/view/templates

echo "customisation done"
