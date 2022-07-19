build:
	make yahwe_zaonhe.dict.yaml
	make qieyun_zaonhe.dict.yaml
	make liangfen.txt
	make TSCharacters.txt
	python main.py

clean:
	rm yahwe_zaonhe.dict.yaml
	rm qieyun_zaonhe.dict.yaml
	rm liangfen.txt
	rm TSCharacters.txt

yahwe_zaonhe.dict.yaml:
	test -f $@ || wget https://cdn.jsdelivr.net/gh/wugniu/rime-yahwe_zaonhe@latest/yahwe_zaonhe.dict.yaml -O $@ --timestamping

qieyun_zaonhe.dict.yaml:
	test -f $@ || wget https://cdn.jsdelivr.net/gh/wugniu/rime-qieyun_zaonhe@latest/qieyun_zaonhe.dict.yaml -O $@ --timestamping

liangfen.txt:
	test -f $@ || wget https://github.com/ayaka14732/liangfen/releases/download/20200724/liangfen.txt -O $@ --timestamping

TSCharacters.txt:
	test -f $@ || wget https://cdn.jsdelivr.net/npm/opencc-data@latest/data/TSCharacters.txt -O $@ --timestamping
