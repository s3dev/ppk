
ifndef dst
    dst=/usr/local/bin
    dst_ppkd=$(dst)/ppk.d/ppk
else
    dst_ppkd="$(dst)"/ppk.d/ppk
endif

all: clean install

install:
	@echo "Installing to: $(dst_ppkd)"
	sudo mkdir -p $(dst_ppkd)
	sudo cp ./requirements.txt $(dst_ppkd)
	sudo cp ./LICENSE $(dst_ppkd)
	sudo cp ./NOTICE $(dst_ppkd)
	sudo cp ./README.md $(dst_ppkd)
	sudo cp ./ppk/__init__.py $(dst_ppkd)
	sudo cp -rv ./ppk/bin $(dst_ppkd)/bin
	sudo cp -rv ./ppk/libs $(dst_ppkd)/libs
	sudo ln -s $(dst_ppkd)/bin/_ppk.sh $(dst)/ppk

clean:
	@if [ -d "$(dst_ppkd)" ]; then \
	    echo "Removing old ppk installation ... "; \
	    sudo rm -rf "$(dst)"/ppk*; \
	    echo "Done."; \
	fi

