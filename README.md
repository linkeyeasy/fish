<!--本项目描述性内容-->
# 配置文件

## editorconfig

> `.editorconfig` 配置基本的文本格式
>
> 如：
>
> `js`、`css`、`json` 配置2个空格
>
> `python` 配置4个空格
>

## setup.cfg

> 配置`flake8`、`isort`等内容
>

### `isort` 安装

> pip install isort

### `isort` 格式化import顺序

```Shell
# 根据本地配置文件`.isort.cfg`, `setup.cfg`
isort -rc .
isort -rc views
```

### `vscode` 安装 isort 插件

> 快捷键 `shift + cmd + p` 打开命令行
>
> 直接输入`isort` 即可格式化本编辑器下python文本

