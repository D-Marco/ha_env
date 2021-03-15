# 使用说明

## 镜像构建说明
本文件用于构建智能家居所需要使用的镜像
* 构建m2m镜像
```shell script
docker build  -f Dockerfile_m2m -t dockerhub.nlecloud.com/1x_virtual_platform/m2m:1.0.0 .
```
* 构建ha镜像
 ha:0.114.4是将homeassistant/home-assistant：0.114.4重新打tag上传到私有仓库的

* 构建mosquitto镜像
mosquitto私有仓库上本来就有，不用构建

## 目录及文件说明
* docker目录下存入执行脚本和compose脚本
* src是m2m程序目录;config.xml文件配置远程和本地的mqttt broker的信息；requirements.txt是程序需要用到的三方库。 
* Dockerfile_m2m是构建m2m程序镜像的脚本
* config.xml是运行m2m容器时挂载的配置文件

## 使用说明
* 如果需要修改m2m程序，则重新构建一下m2m镜像，并提交到仓库仓库上（dockerhub.nlecloud.com），并迭代一个版本；
* 如果不需要修改m2m程序，则直接定位到docker目录下，执行startup.sh来启动相关容器。
