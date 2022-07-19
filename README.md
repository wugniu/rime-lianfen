# rime-lianfen: 上海話兩分

℞: `wugniu/rime-lianfen`

Lianfen (上海話兩分) is the Shanghainese version of Liang-Fen input method.

It is based on [zisea](http://zisea.com/) Liang Fen (字海兩分) data and the dictionaries of the [rime-yahwe_zaonhe](https://github.com/wugniu/rime-yahwe_zaonhe) input method and the [rime-qieyun_zaonhe](https://github.com/wugniu/rime-qieyun_zaonhe) input method.

<p align="center">
  <img src="https://github.com/wugniu/rime-lianfen/blob/main/images/%E9%A9%AB%E9%BA%A4.png?raw=true alt="驫麤" height="250"/>
<p/>

## Install

Get [the `plum` configuration manager](https://github.com/rime/plum), and use it to install:

```shell
bash rime-install wugniu/rime-lianfen
```

Alternatively, copy `lianfen.dict.yaml` and `lianfen.schema.yaml` into your `Rime/` directory.

Finally, ensure that you have activated `lianfen` in your `Rime/default.yaml` configuration file or patch it in your `Rime/default.custom.yaml`:

```yaml
schema_list:
  - { schema: lianfen }
```

## Usage

Input a character by the pronunciation of two parts. For example:

- 蒛 = 艹 (tshau) + 缺 (chiuih) = tshauchiuih
- 蒜 = 艹 (tshau) + 示 (zy) = tshauzy

More detailed rules can be found [here](http://cheonhyeong.com/File/LiangFenHandbook.pdf) (in Chinese).

You can press `v` to enter the Cangjie reverse lookup.

### Customise

You can uncomment rules in `lianfen.schema.yaml` to customise the input method, such as enabling support for the 吳語學堂-style romanisation, or enabling support for new-generation Shanghainese (新派).

## Build

With Python>=3.8 in your environment, simply run:

```shell
make build
```
