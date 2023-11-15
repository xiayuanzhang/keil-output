# 简介

### 使用keil自带的fromelf工具可以将axf文件格式化为bin文件.

该指令就是将 .axf 输出为一个和 .axf 文件同目录下的 .bin 文件

```shell
fromelf --bin -o "$L@L.bin" "#L"
```

指令的具体含义如下

```shell
// --bin = 转换为bin文件
// -o = 制定输出路径
// $P = .uvprojx文件所在路径 //如果有$L就是指.axf文件所在的路径
// @L = keil中 target/Output/Name of Executable 中设置的字符
// #L = keil中 target/Output/Name of Executable 中设置的字符 + .axf 这个文件   
```

.axf文件和 .bin文件的名称在下图所示位置设置

![image-20231115205717268](img/image-20231115205717268.png)

### 该脚本功能

可将指定目录中的 bin hex axf文件添加上版本信息拷贝到指定的输出路径.

`config.json` 配置文件内容如下

所有路径使用相对路径

```json
//只能使用相对路径
//相对路径是output.exe所在路径的相对路径
{
    "keilOutputDir": "../MDK-ARM/Objects", //keil编译输出路径, 从中提取axf文件和.hex文件

    "versionFile": "./version.h", //版本文件
    "versionStr": "#define SOFT_VERSION" , //版本文件中的版本号字符串
  
    "outputDir": "./", //输出路径
  
    "removeHistory": true, //是否删除历史版本
  
    "versionEnable": true, //是否启用版本文件, 不启用示例 filename.bin, 启用示例: filename-version.bin
    "binEnable": true,  //是否拷贝bin文件
    "hexEnable": false,   //是否拷贝hex文件
    "axfEnable": false   //是否拷贝axf文件

}
```
