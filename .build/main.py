from collections import defaultdict
from datetime import datetime
from itertools import chain

NAME = "lianfen"
VERSION = datetime.now().strftime("%Y.%m.%d")
DICT_SEPARATOR = "-"


def main() -> None:
    write_dict()
    write_schema()


def get_freq(s) -> float:
    """
    >>> get_freq('2')
    2.0
    >>> get_freq('2%')
    0.02
    """
    if s[-1] == "%":
        return float(s[:-1]) * 0.01
    else:
        return float(s)


def write_dict() -> None:
    error_keys = set()

    # Traditional Chinese to Simplified Chinese

    with open("TSCharacters.txt") as f:
        d_t2s = {t: s.split(" ") for line in f for t, s in (line.rstrip().split("\t"),)}

    # rime-yahwe_zaonhe and rime-qieyun_zaonhe dictionary data

    d_simp = defaultdict(list)
    d_trad = defaultdict(list)

    with open("yahwe_zaonhe.dict.yaml") as f1, open("qieyun_zaonhe.dict.yaml") as f2:
        # skip the yaml header
        for line in f1:
            if line == "...\n":
                break
        for line in f2:
            if line == "...\n":
                break

        f = chain(f1, f2)

        # dictionary data
        for line in f:
            if line[0] != "#":  # skip comments
                parts = line.rstrip().split("\t")
                char = parts[0]
                if len(char) == 1 and len(parts) > 1:  # restrict to single character
                    # remove pronunciation with low frequency
                    if len(parts) == 2 or get_freq(parts[2]) > 0.07:
                        # replace if a character has two syllables
                        wuphin = parts[1].replace(" ", "")

                        # remove tone from ``qieyun_zaonhe``
                        wuphin = "".join(filter(lambda _: not _.isdigit(), wuphin))

                        # the original Traditional Chinese character
                        d_trad[char].append(wuphin)

                        try:
                            for ch in d_t2s[char]:
                                # Simplified Chinese character
                                d_simp[ch].append(wuphin)
                        except KeyError:
                            ...

    d_simp_trad = {**d_simp, **d_trad}

    # override

    d_override = {}

    with open("override.txt") as f1, open("radicals.txt") as f2:
        for line in chain(f1, f2):
            ch, equiv = line.rstrip().split("\t")

            if equiv.isascii():  # is wuphin
                d_override[ch] = equiv
            else:  # is an equivalent Sinograph
                if wuphin := d_simp_trad.get(equiv):
                    d_override[ch] = wuphin
                else:
                    error_keys.add(equiv)

    # combine dictionaries

    d = {**d_simp_trad, **d_override}

    res = []

    with open("liangfen.txt") as f:
        for line in f:
            ch = line[0]

            try:
                if len(line) == 5:
                    word_l = line[2]
                    word_r = line[3]
                    for wuphin_l in d[word_l]:
                        for wuphin_r in d[word_r]:
                            res.append((ch, f"{wuphin_l}{DICT_SEPARATOR}{wuphin_r}"))
                else:  # len(line) == 4
                    word = line[2]
                    for wuphin in d[word]:
                        res.append((ch, wuphin))
            except KeyError as e:
                cause = e.args[0]
                error_keys.add(cause)

    # write errors

    with open("missing.log", "w") as f:
        for k in sorted(error_keys):
            print(k, file=f)

    # write results

    header = f"""# Rime dictionary
# encoding: utf-8
#
# Lianfen, the Shanghainese version of Liang-Fen (兩分) input method.
#
# Based on zisea Liang Fen (字海兩分) data (https://github.com/ayaka14732/liangfen),
# and the dictionaries of the rime-yahwe_zaonhe input method (https://github.com/wugniu/rime-yahwe_zaonhe)
# and the rime-qieyun_zaonhe input method (https://github.com/wugniu/rime-qieyun_zaonhe).

---
name: {NAME}
version: "{VERSION}"
sort: by_weight
use_preset_vocabulary: true
...
"""

    res = sorted(set(res))

    with open(f"../{NAME}.dict.yaml", "w") as f:
        print(header, file=f)

        for l, r in res:
            print(l, r, sep="\t", file=f)


def write_schema() -> None:
    schema = f"""# Rime schema
# encoding: utf-8

schema:
  schema_id: {NAME}
  name: 上海話兩分
  version: "{VERSION}"
  author:
    - Yuanhao 'Nyoeghau' Chen <nyoeghau@nyoeghau.com>
  description: |-
    The Shanghainese version of Liang-Fen (兩分) input method.
  dependencies:
    - cangjie5

switches:
  - name: ascii_mode
    reset: 0
    states: [中文, 西文]
  - name: full_shape
    reset: 0
    states: [半角, 全角]
  - name: extended_charset
    reset: 1
    states: [通用, 增廣]
  - name: ascii_punct
    reset: 0
    states: [。，, ．，]

engine:
  processors:
    - ascii_composer
    - recognizer
    - key_binder
    - speller
    - punctuator
    - selector
    - navigator
    - express_editor
  segmentors:
    - ascii_segmentor
    - matcher
    - affix_segmentor@cangjie5
    - abc_segmentor
    - punct_segmentor
    - fallback_segmentor
  translators:
    - punct_translator
    - script_translator
    - table_translator@cangjie5
  filters:
    - simplifier
    - uniquifier
    - reverse_lookup_filter

speller:
  alphabet: ;zyxwvutsrqponmlkjihgfedcba
  delimiter: " '"
  algebra:
    - xform/'/;/

    - abbrev/^([a-z]).+$/$1/
    - abbrev/^(([ptsck]|ts)h).+$/$1/
    - abbrev/^(ts).+$/$1/
    - abbrev/^(ny).+$/$1/
    - abbrev/^(ng).+$/$1/
    - abbrev/^(gh).+$/$1/

    # 新派口音
    # - derive/(^|-)tsi/$1ci/
    # - derive/(^|-)tshi/$1chi/
    # - derive/(^|-)([sz])i/$1$2hi/
    # - derive/(^|-)zi/$1ji/
    # - derive/ah($|-)/eh$1/
    # - derive/eh($|-)/ah$1/
    # - derive/ioh($|-)/iuih$1/
    # - derive/iuih($|-)/ioh$1/

    # 中派口音
    - derive/(?<=[sz])yu($|-)/y$1/
    - derive/ae($|-)/e$1/ # 模糊“蘭”“雷”
    - derive/ie($|-)/i$1/ # 模糊“煙”“衣”
    - derive/aeh($|-)/ah$1/ # 多數中派模糊前後ah
    - derive/ah($|-)/aeh$1/
    - derive/aon($|-)/an$1/ # 多數中派模糊前後an
    - derive/an($|-)/aon$1/

    - derive/(^|-)zaon($|-)/$1laon$2/ # 地上、衣裳
    - derive/(^|-)zi(?=a)/$1y/ # 謝謝 zia ya; 好像 hau yan

    # 簡寫以及更多易錯模糊
    - derive/(^|-)ny(?=[aeou])/$1ni/
    - derive/(^|-)nyi/$1ni/
    # - derive/(^|-)sh/$1x/
    # - derive/(^|-)ch/$1q/
    - derive/ui([nh])($|-)/u$1$2/

    # 兼容吳語學堂
    # - derive/(^|-)r($|-)/$1er$2/
    # - abbrev/(^|-)nyi([nh]($|-)|($|-))/$1gni$2/
    # - abbrev/(^|-)ny(?=[aeou])/$1gni/
    # - derive/ui([nh]($|-))/u$1/
    # - derive/h($|-)/q$1/

    - xform/-//

translator:
  dictionary: {NAME}
  spelling_hints: 20

cangjie5:
  tag: cangjie5
  dictionary: cangjie5
  enable_user_dict: false
  prefix: "v"
  suffix: ";"
  tips: 〔倉頡五代〕
  preedit_format:
    - 'xform/^([a-z]*)$/$1\t（\\U$1\\E）/'
    - "xlit|ABCDEFGHIJKLMNOPQRSTUVWXYZ|日月金木水火土竹戈十大中一弓人心手口尸廿山女田難卜符|"
  comment_format:
    - "xlit|abcdefghijklmnopqrstuvwxyz~|日月金木水火土竹戈十大中一弓人心手口尸廿山女田難卜符～|"
  disable_user_dict_for_patterns:
    - "^z.*$"
    - "^yyy.*$"

reverse_lookup:
  tags: [ cangjie5 ]
  overwrite_comment: false
  dictionary: {NAME}

punctuator:
  import_preset: default

key_binder:
  import_preset: default

recognizer:
  import_preset: default
  patterns:
    cangjie5: "^v[a-z]*;?$"
"""
    with open(f"../{NAME}.schema.yaml", "w") as f:
        print(schema, file=f, end="")


if __name__ == "__main__":
    main()
