source .ENV

echo "Apply styling"
echo "copying $CP_THEME_HOME/style content to $CP_HOME/catprez/view/style"
cp $CP_THEME_HOME/style/* $CP_HOME/catprez/view/style

echo "Apply templates"
echo "copying $CP_THEME_HOME/templates content to $CP_HOME/catprez/view/templates"
cp $CP_THEME_HOME/templates/* $CP_HOME/catprez/view/templates

echo "Apply model extensions"
echo "copying $CP_THEME_HOME/model content to $CP_HOME/catprez/model"
cp $CP_THEME_HOME/model/* $CP_HOME/catprez/model

echo "Add plugins"
echo "copying $CP_THEME_HOME/plugins content to $CP_HOME/catprez/plugins"
cp $CP_THEME_HOME/plugins/* $CP_HOME/catprez/plugins

echo "customisation done"
