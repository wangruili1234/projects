import json
from tkinter import *
import os
from tkinter import filedialog
import shutil
import datetime
from tkinter import messagebox
import zipfile
import threading

#ya suo
class optThread(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, dirPath):  
        threading.Thread.__init__(self)
        self.whiteList = ['6879c938-b277-4fd2-8ccb-5152f7fa0ecc.22397.png']
        self.rootDir = dirPath
        self.thread_stop = False 
        
    def recursionOpitimize(self, dirPath):
        resDirs = os.listdir(dirPath)
        for item in resDirs:
            if os.path.isdir(dirPath + os.sep + item):
                self.recursionOpitimize(dirPath + os.sep + item)
            else:
                if self.isCanOpitimize(dirPath + os.sep + item,item) == True:
                    print("\r"+item ,end='')
                    self.OpitimizePng(dirPath + os.sep + item)

    def isCanOpitimize(self,filePath,item):
        fileName, extName = os.path.splitext(filePath)
        if item in self.whiteList:
            print("非压缩白名单："+ item)
            return False
        if extName == '.png' or extName == '.PNG':
            return True
        return False

    def run(self): #Overwrite run() method, put what you want the thread do here  
        print ("开始压缩文件夹：  ",self.rootDir)
        self.recursionOpitimize(self.rootDir)
        self.stop()
            
    def stop(self):  
        self.thread_stop = True
    
    def OpitimizePng(self,filePath):
        cmd = os.getcwd()+'/pngquant/pngquant.exe  --output ' + filePath + ' --force --speed 1 ' + filePath
        os.system(cmd)




svnPath = ""
cocosPath = ""
projectPath = 'D:\worktest\hellotest'
configPath = './config.json'
dyPath = './'
serverRemotePath = './serverRemote'
version = "1.0.0.0"
platform = {}

platforms = [{"key":"wechat","name":"微信","platform":"wechatgame","channelId":"9000"},
             {"key":"bytedance","name":"抖音","platform":"bytedance","channelId":"9015"},
             {"key":"alipay","name":"支付宝小游戏","platform":"alipay","channelId":"9000"},
             {"key":"taobao-minigame","name":"淘宝小游戏","platform":"taobao-minigame","channelId":"9000"},
             {"key":"jingdong","name":"京东","platform":"wechatgame","channelId":"9000"}]
checkValues=[]

def RemoveFile(file):
    if os.path.isfile(file): 
        os.remove(file)

def RemoveDir(dir):
    shutil.rmtree(dir)

def RmoveDirFile(dir):
    resDirs = os.listdir(dir)
    for item in resDirs:
        itemPath = dir+os.sep+item
        if os.path.isdir(itemPath):
            RmoveDirFile(itemPath)
        else:
            RemoveFile(itemPath)

def RmoveDirAndFile(dir):
    if os.path.exists(dir):
        RmoveDirFile(dir)
        RemoveDir(dir)

def saveFile(file,content):
    file = open(file,'w+')
    file.write(str(content))
    file.close()

def initConfig():
    global config
    config = {}
    if os.path.exists(configPath):
         with open(configPath,'rb') as fp:
            data = fp.read()
            config = json.loads(data)

    if ("version" in config) == False:
        print("------------")
        config["version"] = "1.0.0.0"
        config["svnpath"] = ""
        config["projectpath"] = ""
        config["cocospath"] = ""
        config['removeRemote'] = "0"
        config['platform'] = "bytedance"

def saveConfig():
    svnPath =  svnEntryStringVar.get()
    projectPath =  projectEntryStringVar.get()
    cocosPath = cocosEntryStringVar.get()
    removeRemote =  checkValue.get()
    version =  versionEntryStringVar.get()

    config["version"] = version
    config["svnpath"] = svnPath
    config["projectpath"] = projectPath
    config["cocospath"] = cocosPath
    config['removeRemote'] = removeRemote
    config['platform'] = platform["key"]
    saveFile(configPath, json.dumps(config))

def initData():
    global version
    global projectPath
    global svnPath
    global config
    global cocosPath
    global removeRemote
    global platform

    initConfig()

    version =  config["version"]
    svnPath =  config["svnpath"]
    projectPath =  config["projectpath"]
    cocosPath = config["cocospath"]
    removeRemote =  config['removeRemote']

    for data in platforms:
        if data["key"] ==  config['platform']:
            platform = data

def ClickSvnPath():
    global svnPath
    filePath = filedialog.askopenfilename()
    if filePath != "":
        svnPath = filePath
        svnEntryStringVar.set(svnPath)
        saveConfig()

def ClickProjectPath():
    global projectPath
    filePath =  filedialog.askdirectory()
    if filePath != "":
        projectPath = filePath
        projectEntryStringVar.set(projectPath)
        saveConfig()

def ClickCocosPath():
    global cocosPath
    filePath =  filedialog.askopenfilename()
    if filePath != "":
        cocosPath = filePath
    cocosEntryStringVar.set(cocosPath)
    saveConfig()

def ClickSelectValue():
    global removeRemote
    removeRemote = checkValue.get()
    saveConfig()

#修改config中渠道id
def setConfigFile():
    filePath = projectPath +"/assets/scripts/utils/config.js"
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    index = 0
    for line in lines:
        if str(line).find("ChannelID") != -1:
            lines[index] = 'Config.ChannelID = {0};\n'.format(platform["channelId"])
        index += 1
    
    with open(filePath, 'w', encoding='utf-8') as file:
        file.writelines(lines)

threadPool = []
def yaosuoPng(path):
    resDirs = os.listdir(path)
    for item in resDirs:
        if os.path.isdir(path + os.sep + item):
            thread = optThread(path + os.sep + item)
            threadPool.append(thread)

    for thread in threadPool:
        thread.start()
    
    while(True):
      isEnd = True
      for th in threadPool:
          if th.thread_stop == False:
              isEnd = False
      if isEnd:
        threadPool.clear()
        return
   


def buildAll():
    saveConfig()
    if svnPath == "":
        messagebox.showinfo(title="提示",message="请输入svn软件安装地址")
        return
    if projectPath == "":
        messagebox.showinfo(title="提示",message="请输入项目地址")
        return
    if cocosPath == "":
        messagebox.showinfo(title="提示",message="请输入cocos creator编辑器地址")
        return
    updateProject()
    setConfigFile()
    buildPrepare()
    buildDyGame()
    copyBuild()
    showLog("打包完成")

def buildPrepare():
    if platform["key"] == "wechat":
        wxBuildPrepare()
    else:
        print("暂不支持的平台")

def wxBuildPrepare():
    outfile = projectPath +"/assets/localizedRes"
    if os.path.exists(outfile) == True:
        RmoveDirAndFile(outfile)
        RemoveFile(outfile+".meta")
    
    showLog("微信平台准备完成")

def buildDyGame():
    showLog(projectPath+"build 项目"+cocosPath)
    cmd = '"{0}"  --path {1} --build platform={2}'.format(cocosPath,projectPath,platform["platform"])
    result = os.system(cmd)
    print("build end "+ str(result))

def copyBuild():
    saveConfig()
    global version
     #非抖音平台需要压缩png
    if platform["key"] != "bytedance":
        yaosuoPng(projectPath+"/build/"+platform["platform"])
    version =  versionEntryStringVar.get()
    outfile = dyPath+platform["key"]
    if os.path.exists(outfile) == True:
        print("删除旧的工程："+outfile)
        RmoveDirAndFile(outfile)
    print(projectPath+"/build/"+platform["platform"])
    shutil.copytree(projectPath+"/build/"+platform["platform"],outfile)

    showLog("提取远程包资源并生成zip包")
    #将remote文件复制并打包成zip，然后删除抖音工程下的
    if os.path.exists(outfile+"/remote") == True:
        nowTime = datetime.datetime.now()
        remoteOutPath = serverRemotePath+"/"+platform["key"]+"/"+version +"/" +nowTime.strftime("%Y%m%d")
        code = dirCount(remoteOutPath)
        remoteOutPath = remoteOutPath + "/"+nowTime.strftime("%H%M")
        if os.path.exists(remoteOutPath) == True:
            RmoveDirAndFile(remoteOutPath)
        print("创建远程包目录："+remoteOutPath)
        shutil.copytree(outfile+"/remote",remoteOutPath+"/remote")
        if platform["key"] == "bytedance":
            zip_name = 'remote{0}v{1}r{2}_dy.zip'.format(nowTime.strftime("%Y%m%d"),version,code)
        elif platform["key"] == "taobao-minigame":
            zip_name = 'remote_{0}_taobao_{1}.zip'.format(version,nowTime.strftime("%Y%m%d"))
        elif platform["key"] == "alipay": 
            zip_name = 'remote_{0}_zhifubao_{1}.zip'.format(version,nowTime.strftime("%Y%m%d"))
        elif platform["key"] == "jingdong":
            zip_name = 'remote_{0}_jingdong_{1}.zip'.format(version,nowTime.strftime("%Y%m%d"))
        else:
            zip_name = 'remote{0}v{1}r{2}_{3}.zip'.format(nowTime.strftime("%Y%m%d"),version,code,platform["key"])
        createZip(remoteOutPath,remoteOutPath,zip_name)
    if removeRemote == "1":
        RmoveDirAndFile(outfile+"/remote")
        
    if platform["key"] == "bytedance":
        dyBuildTrailing()
    elif platform["key"] == "wechat":
        wxBuildTrailing()
    saveConfig()
    messagebox.showinfo(title="提示",message="打包完成")
    showLog("流程结束")

def copyBuildScript():
    srcPath = projectPath+"/build/"+platform["platform"]+"/src/scripts"
    toPath = dyPath+platform["key"]+"/src/scripts"
    if os.path.exists(toPath) == True:
        RmoveDirAndFile(toPath)
    shutil.copytree(srcPath,toPath)
    messagebox.showinfo(title="提示",message="脚本文件已复制到打包目录")

def zipFile(_path,zipf):
    for root,dirs,files in os.walk(_path):
        for file in files:
            file_path = os.path.join(root,file)
            zipf.write(file_path,os.path.relpath(file_path,_path))

def createZip(_path,_zip_path,_zip_name):
     with zipfile.ZipFile(_zip_path +"/"+ _zip_name,'a',zipfile.ZIP_DEFLATED) as zipf:
         zipFile(_path,zipf)

#更新项目
def updateProject():
    showLog("更新项目"+svnPath)
    cmd = '"{0}"/command:update /path:{1} /closeonend:2'.format(svnPath,projectPath)
    os.system(cmd)

def showLog(msg):
    logLabel["text"] = msg
    print(msg)

def selectPlatform(key):
    print(key)
    global platform
    index = 0
    for _plat in platforms:
        if _plat["key"] == key:
            platform = _plat
        else:
            checkValues[index].set("0")
        index += 1
    saveConfig()

#微信平台需要额外处理
def wxBuildTrailing():
    #拷贝
    copyTopath=dyPath+platform["key"]+"/src/myOpenDataContext"
    shutil.copytree(dyPath+'platform/wechat/openDataContext',copyTopath)

    #拷贝文件替换原来文件
    shutil.copy(dyPath+'platform/wechat/white.json',dyPath+platform["key"]+"/game.json")
    shutil.copy(dyPath+'platform/wechat/project.config.json',dyPath+platform["key"]+"/project.config.json")
    print("微信平台额外处理完成")

def dyBuildTrailing():
    #game.json中加入
    filePath = dyPath +platform["key"]+"/game.json"
    print(filePath)
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines.insert(3,'    "enableIOSHighPerformanceMode": true,\n')
    with open(filePath, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def dirCount(dirPath):
    count = 0
    if os.path.exists(dirPath) == False:
        return count
    dirs = os.listdir(dirPath)
    for dir in dirs:
        if os.path.isdir(os.path.join(dirPath,dir)):
            count += 1
    return count

def ui():
    global logLabel
    global svnEntryStringVar
    global projectEntryStringVar
    global versionEntryStringVar
    global cocosEntryStringVar
    global checkValue
    global checkValues
    initData()

    viewRoot = Tk()
    viewRoot.title("Creator项目打包")
    viewRoot.geometry("600x300")

    label = Label(viewRoot,text="",font=24)
    label.pack()

    frame1 = Frame(viewRoot)
    frame1.pack(side=TOP,anchor=N,pady=0,expand=YES,fill=BOTH)
    svnLabel = Label(frame1,text='SVN安装地址')
    svnLabel.pack(side=LEFT,anchor=W)
    svnEntryStringVar = StringVar(value=svnPath)
    svnPathEntry = Entry(frame1,textvariable=svnEntryStringVar,width=50)
    svnPathEntry.pack(side=LEFT,anchor=W)
    svnPathButton  = Button(frame1,text="...",command=ClickSvnPath,width=10)
    svnPathButton.pack(side=LEFT,anchor=W,padx=5)

    frame3 = Frame(viewRoot)
    frame3.pack(side=TOP,anchor=N,pady=0,expand=YES,fill=BOTH)
    cocosLabel = Label(frame3,text='cocos creator 安装地址：')
    cocosLabel.pack(side=LEFT,anchor=W)
    cocosEntryStringVar = StringVar(value=cocosPath)
    cocosPathEntry = Entry(frame3,textvariable=cocosEntryStringVar,width=40)
    cocosPathEntry.pack(side=LEFT,anchor=W)
    cocosPathButton  = Button(frame3,text="...",command=ClickCocosPath,width=10)
    cocosPathButton.pack(side=LEFT,anchor=W,padx=5)

    frame2 = Frame(viewRoot)
    frame2.pack(side=TOP,anchor=N,pady=0,expand=YES,fill=BOTH)
    projectLabel = Label(frame2,text='输入项目工程地址')
    projectLabel.pack(side=LEFT,anchor=W)
    projectEntryStringVar = StringVar(value=projectPath)
    projectPathEntry = Entry(frame2,textvariable=projectEntryStringVar,width=40)
    projectPathEntry.pack(side=LEFT,anchor=W)
    projectPathButton  = Button(frame2,text="...",command=ClickProjectPath,width=10)
    projectPathButton.pack(side=LEFT,anchor=W,padx=5)

    frame3 = Frame(viewRoot)
    frame3.pack(side=TOP,anchor=N,pady=0,expand=YES,fill=BOTH)
    versionLabel = Label(frame3,text='输入当前版本号：')
    versionLabel.pack(side=LEFT,anchor=W)
    versionEntryStringVar = StringVar(value=version)
    versionEntry = Entry(frame3,textvariable=versionEntryStringVar,width=50)
    versionEntry.pack(side=LEFT,anchor=W)

    frame4 = Frame(viewRoot)
    frame4.pack(side=TOP,anchor=N,pady=0,expand=YES,fill=BOTH)
    for _platform in platforms:
       if _platform["key"] == platform["key"]:
            checkV = create_checkbutton(frame4,_platform["name"],_platform["key"],"1")
       else:
            checkV = create_checkbutton(frame4,_platform["name"],_platform["key"],"0")   
       checkValues.append(checkV)

    checkValue = StringVar()
    checkValue.set(removeRemote)
    checkbutton = Checkbutton(viewRoot,text="是否删除工程下的remote",command=ClickSelectValue,variable=checkValue,onvalue="1",offvalue="0",font=("size",16))
    checkbutton.pack(side=TOP,anchor=W)

    buildButton  = Button(viewRoot,text="开始打包",command=buildAll,width=10)
    buildButton.pack(side=LEFT,pady=5)

    buildButton1  = Button(viewRoot,text="仅执行打包后续",command=copyBuild,width=20)
    buildButton1.pack(side=LEFT,pady=10,padx=10)

    buildButton2  = Button(viewRoot,text="仅同步代码",command=copyBuildScript,width=20)
    buildButton2.pack(side=LEFT,anchor=N,pady=10)

    buildButton3  = Button(viewRoot,text="测试",command=wxBuildTrailing,width=20)
    buildButton3.pack(side=LEFT,anchor=N,pady=10)

    logLabel = Label(viewRoot,text='耐心等待',font=24)
    logLabel.pack(side=TOP,anchor=CENTER,pady=10,padx=10)

    viewRoot.mainloop()

def create_checkbutton(root,text,key,defaultValue):
    checkValue = StringVar()
    checkValue.set(defaultValue)
    checkbutton = Checkbutton(root,text=text,command=lambda:selectPlatform(key),variable=checkValue,onvalue="1",offvalue="0",font=("size",16))

    checkbutton.pack(side=LEFT,anchor=W,expand=YES,fill=BOTH)
    return checkValue


if __name__ == "__main__":
    ui()