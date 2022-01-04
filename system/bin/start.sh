if [ ! -f "eula.txt" ];then
  cp ../system/config/eula.txt eula.txt
fi

if [ ! -f "server.properties" ];then
  cp ../system/config/server.properties server.properties
fi

java -jar ../system/bin/server.jar & java -jar ../system/bin/Geyser.jar

