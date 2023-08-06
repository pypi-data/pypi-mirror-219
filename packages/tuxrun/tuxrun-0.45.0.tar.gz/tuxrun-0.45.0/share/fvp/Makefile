LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.21_15"
morello_version ?= "0.11_34"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --tag fvp:morello-$(container_morello_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
