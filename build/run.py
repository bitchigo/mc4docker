import json
import urllib.request
import datetime
import os

githubActionPath="/home/runner/work/mc4docker/mc4docker/"
githubActionRunPath=githubActionPath+"build/"
jarDownLoadUrl="https://bmclapi2.bangbang93.com/version/#version/server"
jarDownLoadUrlVersionPlaceHolder="#version"
jarSavePath=githubActionRunPath+"../system/bin/server.jar"
getVersionsUrl="http://launchermeta.mojang.com/mc/game/version_manifest.json"

# 检查是否存在大于上次执行的时间版本 节约资源
def readLastBuildTime():
    file= open(githubActionRunPath+"./runtime.txt",encoding='utf-8')
    content=file.read()
    print("上次系统构建时间为:"+ content+"\n")
    file.close()
    lastBuildTime = datetime.datetime.strptime(content,"%Y%m%d")
    return lastBuildTime
    
    

def getVersion():
    print("正在获取版本信息\n")
    response = urllib.request.urlopen(getVersionsUrl)
    versionjsonStr=response.read()
    print("版本信息为"+str(versionjsonStr)+"\n")
    data = json.loads(versionjsonStr)
    lastVersion=data["latest"]["release"]
    versions=data["versions"]
    return lastVersion,versions


def main():
    lastBuildTime = readLastBuildTime()

    lastVersion,versions = getVersion()
    print("最后发行正式版本为"+lastVersion+"\n")
    lastVersionTime= lastBuildTime
    for version in versions:
        timeStr=version["time"]
        time = datetime.datetime.strptime(timeStr,"%Y-%m-%dT%H:%M:%S+00:00")
        id=version["id"]
        if lastVersionTime > time:
            print(id+" 版本已经被构建过 跳过\n")
            lastVersionTime = time
        if lastBuildTime < time:
            downloadJarFile(jarDownLoadUrl.replace(jarDownLoadUrlVersionPlaceHolder,id))
            if id == lastVersion:
                buildDocker("lastest")
                pushDocker("lastest")
            buildDocker(id)
            pushDocker(id)

        
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
    main()
