PKGNAME=sugarstick-creator
PKGRPMFLAGS=--define "_topdir ${PWD}" --define "_specdir ${PWD}" --define "_sourcedir ${PWD}/dist" --define "_srcrpmdir ${PWD}" --define "_rpmdir ${PWD}" --define "_builddir ${PWD}"

dist:
	python setup.py sdist --format=bztar

srpm: dist
	@rpmbuild -bs ${PKGRPMFLAGS} ${PKGNAME}.spec

rpm: dist
	cp dist/* ~/rpmbuild/SOURCES/
	cp *.spec ~/rpmbuild/SPECS/
	rpmbuild -ba ~/rpmbuild/SPECS/sugarstick-creator.spec

gui:
	pyrcc4 data/resources.qrc -o sugarstick/resources_rc.py
	pyuic4 data/sugarstick-creator.ui -o sugarstick/linux_dialog.py
	cp sugarstick/linux_dialog.py sugarstick/windows_dialog.py

pyflakes:
	pyflakes sugarstick/*.py

pylint:
	pylint sugarstick/*.py

pot:
	cd po; python mki18n.py -v --domain=sugarstick-creator -p
	#cd po ; intltool-update --pot -g sugarstick-creator

mo:
	cd po; for po in `ls *.po`; do cp $$po sugarstick-creator_$$po; done
	cd po; python mki18n.py -v --domain=sugarstick-creator -m
	rm po/sugarstick-creator_*.po*

clean:
	rm -f *.py{c,o} */*.py{c,o} */*/*.py{c,o}
	rm -fr po/${PKGNAME}*.po{,.new} po/locale
	rm -fr build

docs:
		epydoc --name sugarstick-creator -u http://sugarstick-creator.fedorahosted.org -o docs --exclude urlgrabber sugarstick


everything:
	python setup.py  sdist --format=bztar
	rm -f ~/rpmbuild/RPMS/noarch/sugarstick-creator*.rpm
	make clean rpm
	# sudo rpm -e sugarstick-creator
	sudo rpm -Uvh ~/rpmbuild/RPMS/noarch/sugarstick-creator*.rpm
	sudo /usr/bin/sugarstick-creator -v
