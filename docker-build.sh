echo "clone CatPrez dir to deploy"
mkdir $CP_HOME/deploy
cp -r $CP_HOME/catprez/* $CP_HOME/deploy

echo "Copy my data to CatPrez"
rm $CP_HOME/deploy/cache/*.p
rm $CP_HOME/deploy/data/*
cp -r data/* $CP_HOME/deploy/data

echo "Apply styling"
cp $CP_THEME_HOME/style/* $CP_HOME/deploy/view/style

echo "Apply templates"
cp $CP_THEME_HOME/templates/* $CP_HOME/deploy/view/templates

echo "Apply model extensions"
cp $CP_THEME_HOME/model/* $CP_HOME/deploy/model

echo "Add plugins"
cp $CP_THEME_HOME/plugins/* $CP_HOME/deploy/plugins

echo "Run Docker there"
docker build -t catprez-profcat -f $CP_HOME/Dockerfile $CP_HOME

echo "Clean-up"
rm -r $CP_HOME/deploy

echo "complete"