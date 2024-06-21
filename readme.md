# 功能说明
用于在编译之后, 自动读取指定的头文件中设置的版本号
将该版本号增加到输出的 hex,bin,lib,axf文件中
并且将这些文件 拷贝到指定的输出文件夹
可以选择只操作其中的部分后缀的文件
# 脚本编译说明

打包成exe的工具
```python
# 安装工具包
pip install pyinstaller

#打包指令
pyinstaller -F -w  main.py -n output

# -w表示屏蔽黑窗口, 如果需要使用到命令行(比如printf输出) 就不能加-w
# py_word.py 表示需要打包为exe文件的python脚本
# -n NAME 指定输出的exe文件的名称, 加不加.exe都一样
```

![Alt text](img\image.png)

# 如何生成bin文件

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

# 配置相关
查看模板配置文件 config.ini 及其注释