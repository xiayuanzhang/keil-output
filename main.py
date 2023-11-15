import commentjson
import re
import os, sys
import shutil

#pyinstaller -w -F --name output main.py

def load_config(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()

        config = commentjson.loads(data)

        baseDir = os.path.dirname(filepath)

        keilOutputDir = config.get('keilOutputDir')
        keilOutputDir = os.path.join(baseDir, keilOutputDir)

        versionFile = config.get('versionFile')
        versionFile = os.path.join(baseDir, versionFile)
        versionStr = config.get('versionStr')

        outputDir = config.get('outputDir')
        outputDir = os.path.join(baseDir, outputDir)

        removeHistory = config.get('removeHistory')
        versionEnable = config.get('versionEnable')
        binEnable = config.get('binEnable')
        hexEnable = config.get('hexEnable')
        axfEnable = config.get('axfEnable')

        # print(f'keilOutputDir: {keilOutputDir}')
        # print(f'versionFile: {versionFile}')
        # print(f'versionStr: {versionStr}')
        # print(f'outputDir: {outputDir}')
        # print(f'removeHistory: {removeHistory}')
        # print(f'versionEnable: {versionEnable}')
        # print(f'binEnable: {binEnable}')
        # print(f'hexEnable: {hexEnable}')
        # print(f'axfEnable: {axfEnable}')

        with open(versionFile, 'r', encoding='utf-8') as vf:
            versionData = vf.read()
        pattern = re.compile(f'{versionStr} "(.*?)"')
        match = pattern.search(versionData)
        if match:
            version = match.group(1)
            print(f'version: {version}')
        else:
            version = ''
            print('No version found.')

        # 如果removeHistory为True，删除历史文件
        if removeHistory:
            for enable, ext in [(binEnable, 'bin'), (hexEnable, 'hex'), (axfEnable, 'axf')]:
                if enable:
                    for filename in os.listdir(outputDir):
                        if filename.endswith(f'.{ext}'):
                            os.remove(os.path.join(outputDir, filename))
                            print(f'Deleted {os.path.join(outputDir, filename)}')

        # 搜索并复制文件
        for enable, ext in [(binEnable, 'bin'), (hexEnable, 'hex'), (axfEnable, 'axf')]:
            if enable:
                files = [f for f in os.listdir(keilOutputDir) if f.endswith(f'.{ext}')]
                if len(files) == 0:
                    print(f'No .{ext} file found.')
                elif len(files) > 1:
                    print(f'Please ensure there is only one .{ext} file.')
                else:
                    filename = files[0]
                    if versionEnable and version:
                        new_filename = f'{filename.rsplit(".", 1)[0]}-{version}.{ext}'
                    else:
                        new_filename = filename
                    shutil.copy(os.path.join(keilOutputDir, filename), os.path.join(outputDir, new_filename))
                    print(f'Copied {os.path.join(keilOutputDir, filename)} to {os.path.join(outputDir, new_filename)}')

    except FileNotFoundError:
        print(f'Error: The file [config.json] or [versionFile] does not exist.')
    except KeyError as e:
        print(f'Error: The key {e} does not exist in the JSON file.')



# 使用函数
if __name__ == "__main__":
    current_path = os.path.dirname(sys.argv[0])
    config_path = os.path.join(current_path, "config.json")
    print("config.json dir: ", config_path)
    load_config(config_path)
