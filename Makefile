refresh:
	make clean
	make build

build:
	cd .build && make $@

clean:
	cd .build && make $@
	rm lianfen.dict.yaml
	rm lianfen.schema.yaml
