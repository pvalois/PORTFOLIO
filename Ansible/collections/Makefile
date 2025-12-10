build:
	ansible-galaxy collection build pepiniere/freebox --force
install:
	ansible-galaxy collection install pepiniere-freebox-1.0.0.tar.gz --force
check:
	ansible-galaxy collection list | grep pepiniere
check-doc: 
	ansible-doc pepiniere.freebox.list_dhcp
	ansible-doc pepiniere.freebox.static_lease
all: build install check-doc
