from configparser import ConfigParser, ExtendedInterpolation
import os
import shutil
import sys  # 添加这个导入


#获取命令行输入参数
if len(sys.argv) != 2:
    print('[output]: error: invalid input arguments. End of execution. ')
    sys.exit(0)

# 获取起始路径,并替换路径中的 \ 为 /
config_file = sys.argv[1]
config_file = config_file.replace('\\', '/')
if not os.path.isfile(config_file):
    print('[output]: error: invalid input arguments. End of execution. ')
    sys.exit(0)


# 检测配置文件是否存在
if not os.path.exists(config_file):
    print('[output]: error: config.ini not found. End of execution. ')
    sys.exit(0)

print('[output]: Start, Begin to execute...')

# 读取配置文件
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(config_file,encoding="utf-8")

config_path = os.path.dirname(config_file) + '/'
print('[output]: config_file = ', config_file)

# 检测配置文件中参数是否存在
if not config.has_section('D'):
    print('[output]: error: [D] section not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'print_log'):
    print('[output]: error: print_log not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'keil_output_path'):
    print('[output]: error: keil_output_path not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'copy_bin'):
    print('[output]: error: copy_bin not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'copy_hex'):
    print('[output]: error: copy_hex not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'copy_axf'):
    print('[output]: error: copy_axf not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'output_path'):
    print('[output]: error: output_path not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'version_h'):
    print('[output]: error: version_h not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'version_str'):
    print('[output]: error: version_str not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'version_h_encoding'):
    print('[output]: error: version_h_encoding not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'delete_history'):
    print('[output]: error: delete_history not found. End of execution. ')
    sys.exit(0)
if not config.has_option('D', 'append_version'):
    print('[output]: error: append_version not found. End of execution. ')
    sys.exit(0)

# 获取配置参数
print_log = config.getboolean('D', 'print_log')
keil_output_path = config.get('D', 'keil_output_path')
copy_bin = config.getboolean('D', 'copy_bin')
copy_hex = config.getboolean('D', 'copy_hex')
copy_axf = config.getboolean('D', 'copy_axf')
output_path = config.get('D', 'output_path')
version_h = config.get('D', 'version_h')
version_str = config.get('D', 'version_str')
version_h_encoding = config.get('D', 'version_h_encoding')
delete_history = config.getboolean('D', 'delete_history')
append_version = config.getboolean('D', 'append_version')

if print_log:
    print('[output]: keil_output_path = ', keil_output_path)
    print('[output]: copy_bin = ', copy_bin)
    print('[output]: copy_hex = ', copy_hex)
    print('[output]: copy_axf = ', copy_axf)
    print('[output]: output_path = ', output_path)
    print('[output]: version_h = ', version_h)
    print('[output]: version_str = ', version_str)
    print('[output]: version_h_encoding = ', version_h_encoding)
    print('[output]: delete_history = ', delete_history)
    print('[output]: append_version = ', append_version)

keil_output_path = config_path + keil_output_path
output_path = config_path + output_path
version_h = config_path + version_h

# 检测路径是否存在
if not os.path.exists(keil_output_path):
    print('[output]: error: keil_output_path not found. End of execution. ')
    sys.exit(0)
#如果version_str = "xxx",则将其转换为version_str = xxx
if version_str.startswith('"') and version_str.endswith('"'):
    version_str = version_str[1:-1]
    print('[output]: version_str = ', version_str)

# 判断output_path是否存在，不存在则创建. 存在并且需要删除历史文件, 则删除其中
# 后缀为 .bin .hex .axf .lib 的文件
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print('[output]: output_path not found, create it. ')
else:
    if delete_history:
        for root, dirs, files in os.walk(output_path):
            for file in files:
                if file.endswith('.bin') or file.endswith('.hex') or file.endswith('.axf') or file.endswith('.lib'):
                    os.remove(os.path.join(root, file))
                    print('[output]: delete file: ', os.path.join(root, file))
#如果append_output为True,则获取output_h中的output_str,并记录下来
#output_str的格式为: #define output_STR "V1.0.0"
#或者 #define output_STR                "V1.0.0"
version_num = ''
if append_version:
    if os.path.exists(version_h):
        with open(version_h, 'r',encoding=version_h_encoding) as f:
            lines = f.readlines()
            for line in lines:
                if version_str in line and '#define' in line:
                    if print_log:
                        print('[output]: version_str = ', line)
                        print('[output]: version_str = ', line.split('"'))
                    version_num = line.split('"')[1]
                    break
        print('[output]: version_num = ', version_num)
    else:
        print("[output]: error: version_h = {0} not found. End of execution.".format(version_h))
        sys.exit(0)

# 拷贝文件: 搜索keil_output_path是否最多只有一个 .bin .hex .axf .lib 文件
# 如果 copy_bin copy_hex copy_axf 为 True, 则判断
# 如果不存在该后缀的文件,则跳过,存在则拷贝到output_path
# 如果存在多个, 则报出该后缀的警告, 并且跳过
if copy_bin:
    bin_files = []
    for root, dirs, files in os.walk(keil_output_path):
        for file in files:
            if file.endswith('.bin'):
                bin_files.append(os.path.join(root, file))
    if len(bin_files) == 0:
        print('[output]: warning: no .bin file found. ')
    elif len(bin_files) == 1:
        if append_version:
            filename = os.path.basename(bin_files[0]).split('.')
            namebuffer = '-' + version_num + '.' + filename[-1]
            filename.remove(filename[-1])
            filename = '.'.join(filename) + namebuffer
            shutil.copy(bin_files[0], output_path + '/' + filename)
            print('[output]: copy .bin file and append output: ', output_path + '/' + filename)
        else:
            shutil.copy(bin_files[0], output_path)
            print('[output]: copy .bin file: ', bin_files[0])
    else:
        print('[output]: warning: more than one .bin file found. ')
if copy_hex:
    hex_files = []
    for root, dirs, files in os.walk(keil_output_path):
        for file in files:
            if file.endswith('.hex'):
                hex_files.append(os.path.join(root, file))
    if len(hex_files) == 0:
        print('[output]: warning: no .hex file found. ')
    elif len(hex_files) == 1:
        if append_version:
            filename = os.path.basename(hex_files[0]).split('.')
            namebuffer = '-' + version_num + '.' + filename[-1]
            filename.remove(filename[-1])
            filename = '.'.join(filename) + namebuffer
            shutil.copy(hex_files[0], output_path + '/' + filename)
            print('[output]: copy .hex file and append output: ', output_path + '/' + filename)
        else:
            shutil.copy(hex_files[0], output_path)
            print('[output]: copy .hex file: ', hex_files[0])
    else:
        print('[output]: warning: more than one .hex file found. ')
if copy_axf:
    axf_files = []
    for root, dirs, files in os.walk(keil_output_path):
        for file in files:
            if file.endswith('.axf'):
                axf_files.append(os.path.join(root, file))
    if len(axf_files) == 0:
        print('[output]: warning: no .axf file found. ')
    elif len(axf_files) == 1:
        if append_version:
            filename = os.path.basename(axf_files[0]).split('.')
            namebuffer = '-' + version_num + '.' + filename[-1]
            filename.remove(filename[-1])
            filename = '.'.join(filename) + namebuffer
            shutil.copy(axf_files[0], output_path + '/' + filename)
            print('[output]: copy .axf file and append output: ', output_path + '/' + filename)
        else:
            shutil.copy(axf_files[0], output_path)
            print('[output]: copy .axf file: ', axf_files[0])
    else:
        print('[output]: warning: more than one .axf file found. ')
        
print('[output]: Success, End of execution. ')


