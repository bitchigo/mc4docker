import json
import urllib.request
import datetime
import os
import sys

githubActionPath="/home/runner/work/mc4docker/mc4docker/"
githubActionRunPath=githubActionPath+"build/"
jarSavePath=githubActionRunPath+"../system/bin/server.jar"
getVersionsUrl="http://launchermeta.mojang.com/mc/game/version_manifest.json"

# 检查是否存在大于上次执行的时间版本 节约资源
def readLastBuildTime(timeApi):
    print("正在获取上次更新时间\n")
    # response = urllib.request.urlopen(timeApi+"mcUpdateTime")
    # lastBuildTimeStr=response.read()
    lastBuildTimeStr = "1999-06-12T13:25:51+00:00"
    print("上次更新时间为:"+lastBuildTimeStr+"\n")
    lastBuildTime = datetime.datetime.strptime(lastBuildTimeStr,"%Y-%m-%dT%H:%M:%S+00:00")
    return lastBuildTime,lastBuildTimeStr

def setUpdateTime(timeStr,timeApi):
    urllib.request.urlopen(timeApi+"set/mcUpdateTime/"+timeStr)
    return
    
    

def getVersion():
    print("正在获取版本信息\n")
    response = urllib.request.urlopen(getVersionsUrl)
    versionjsonStr=response.read()
    print("版本信息为"+str(versionjsonStr)+"\n")
    data = json.loads(versionjsonStr)
    lastVersion=data["latest"]["release"]
    versions=data["versions"]
    return lastVersion,versions


def main(args):
    lastBuildTime,lastBuildTimeStr = readLastBuildTime(args[0])
    lastVersion,versions = getVersion()
    print("最后发行正式版本为"+lastVersion+"\n")
    lastVersionTime= lastBuildTime
    lastVersionTimeStr = lastBuildTimeStr
    for version in versions:
        timeStr=version["time"]
        time = datetime.datetime.strptime(timeStr,"%Y-%m-%dT%H:%M:%S+00:00")
        id=version["id"]
        jsonurl=version["url"]
        jsonurlResponse = urllib.request.urlopen(jsonurl)
        jsonurlResponseJsonStr=jsonurlResponse.read()
        jsonurlResponseJsonStrDate = json.loads(jsonurlResponseJsonStr)
        downloadUrl = jsonurlResponseJsonStrDate["downloads"]["server"]["url"]
        if lastVersionTime > time:
            print(id+" 版本已经被构建过 跳过\n")
            lastVersionTime = time
            lastVersionTimeStr= timeStr
        if lastBuildTime < time:
            downloadJarFile(downloadUrl)
            if id == lastVersion:
                buildDocker("lastest")
                pushDocker("lastest")
            buildDocker(id)
            pushDocker(id)
    setUpdateTime(lastVersionTimeStr ,args[0])

        
def buildDocker(id):
    print("正在构建docker 版本:"+id+"\n")
    os.system('docker build -t bitchigo/mc-server:'+id +" githubActionPath")
    print("构建docker成功 版本:"+id+"\n")
    return 

def pushDocker(id):
    print("正在推送docker 版本:"+id+"\n")
    os.system('docker push bitchigo/mc-server:'+id)
    print("推送docker成功 版本:"+id+"\n")
    return 

def downloadJarFile(jarUrl):
    print("正在下载jar文件 "+ jarUrl)
    urllib.request.urlretrieve(jarUrl, jarSavePath)
    print("下载完毕")


if __name__ == "__main__":
    main(sys.argv[1:])
