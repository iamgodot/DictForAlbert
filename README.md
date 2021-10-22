# DictForAlbert

Simple dictionary plugin for Albert based on Python &amp; Youdao Dict.

## Features

- Translation between English and Chinese
- Customizable code to extend functions easily
- Click `Enter` to open Youdao query page in browser

## Usage

```bash
cd $HOME/.local/share/albert/org.albert.extension.python/modules
git clone https://github.com/iamgodot/DictForAblert
```

另外需要配置好有道查询 API 使用的 token:

1. 在[有道智云平台](https://ai.youdao.com/#/)上面注册
2. 创建应用并复制 app_key 和 app_secret
3. 打开 `config.ini` 并填入（注意不要加引号）

重启 albert，进入 Extensions 打开 Python 下面的 Dictionary for Albert.
呼出 albert 键入 `d piano` 就可以看见相关翻译，中文同理。按下回车键会打开有道的网页查询结果页面。

关于 trigger key 的定义默认为 `d`，需要的话直接在代码里修改 `__trigger__` 就好。

## Contributing

Welcome forks and pull requests, or ask any questions in issue page.
