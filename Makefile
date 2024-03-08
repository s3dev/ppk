
ifndef dst
    dst=/usr/local/bin
    dst_ppkd=$(dst)/ppk.d
else
    dst_ppkd="$(dst)"/ppk.d
endif

all: clean install

install:
	@echo "Installing to: $(dst_ppkd)"
	sudo mkdir $(dst_ppkd)
	sudo cp ./requirements.txt $(dst_ppkd)
	sudo cp ./LICENSE $(dst_ppkd)
	sudo cp ./NOTICE $(dst_ppkd)
	sudo cp ./README.md $(dst_ppkd)
	sudo cp -r ./bin $(dst_ppkd)/bin
	sudo cp -r ./lib $(dst_ppkd)/lib
	sudo ln -s $(dst_ppkd)/bin/_ppk.sh $(dst)/ppk

clean:
	@if [ -d "$(dst_ppkd)" ]; then \
	    echo "Removing old ppk installation ... "; \
	    sudo rm -rf "$(dst)"/ppk*; \
	    echo "Done."; \
	fi

