# 91pron_python
利用python3，爬取并下载91pron网站上面的视频
该脚本支持一下功能：
* 支持多线程
* 下载视频有进度条显示
* 支持从特定页的特定视频开始下载
* 将m3u8和mp4格式的视频下载到不同文件夹，加以分类
* 自动过滤已经下载过的视频

由于91pron的网站性质，不挂代理直接爬取的话，网速会比较慢，我都是挂代理，开全局模式进行下载，速度基本跑满，如果有兄弟没有代理的话，我平常在[这个网站](https://paofu.cloud/auth/register?code=Wdie)买流量，还挺实惠的。有需要的可以用我的链接。

# 使用方法
* 首先需要安装python最新版，这里不再教学，网上有很多
* 安装必要包，脚本文件头部有引用。安装命令：`pip install 包名`
* 建议在vs code编辑器，打开项目的demo文件夹，不要直接打开根目录，然后按`F5`，进入bebug模式

当编译器底部出现如下界面，就代表程序运行成功：  
<img src="https://s3.ax1x.com/2021/01/17/sr5exJ.png" alt="运行成功.png" width="100%" height="150" border="0" />

# 需要注意的是
由于91pron网站改版，最新的视频采用m3u8格式，本脚本自动将含有m3u8格式的视频链接保存在当前目录的`urlwithtitle.txt`文本中，每一行用`----`，将内容分割，左边为视频的url，右边为视频的标题，如图所示：  
<img src="https://s3.ax1x.com/2021/01/17/sr5JRe.png" alt="保存的视频链接格式" width="100%" height="150" border="0" />

然后在项目的根目录找到`m3u8DL-CLI`这个文件夹，打开它，双击`N_m3u8DL-CLI-SimpleG.exe`程序，将`urlwithtitle.txt`拖拽到`M3U8地址`栏中，点击`GO`按钮，程序就自动下载分片，最后合并视频  
<img src="https://s3.ax1x.com/2021/01/17/sr5ri8.png" alt="使用方法" width="70%" height="700" border="0" />

下载下来的视频最终保存在`m3u8DL-CLI`这个文件夹的`Downloads`文件夹里，打开以后，会发现，视频都是是带有字符串，不是我们想要的，这时候只需要运行一下`m3u8DL-CLI`目录下的`rename.py`脚本即可完成重命名. **说明一点，重命名后的视频，需要剪切到根目录的`91视频`文件夹中，并将`urlwithtitle.txt`文件内容清空，这么做是为了保证下次运行脚本，过滤已经下载的视频，这点很重要！！！**

下载mp4格式的视频就没有这些问题，直接下载，程序也会有进度条显示，不需要额外操作。
