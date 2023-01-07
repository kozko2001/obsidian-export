all: clean import

clean:
	rm -rf tmp/


import:
	mkdir tmp
	@[ "${DROPBOX_ACCESS_TOKEN}" ] || ( echo ">> DROPBOX_ACCESS_TOKEN is not set"; exit 1 )
	cd export ; npm install; node index.js

	unzip export/data.zip -d tmp/zip
	mv -f tmp/zip/obsidian-notes/* tmp/zip/
	rm export/data.zip
	rm -rf tmp/zip/obsidian-notes


.PHONY: transform
transform:
	rm -rf tmp/content
	python -m pip install setuptools
	python -m pip install -r transform/requirements.txt
	mkdir tmp/content
	mkdir tmp/content/images

	find tmp/zip -name \*.md -exec python3 transform/blog.py -i {} -o ./tmp/content/ -p ./tmp/content/images \;
