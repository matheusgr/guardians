cd src/guardians/qt
pyrcc4 icons.qrc > ../gui/icons_rc.py
pyuic4 main.ui > ../gui/main.py
pyuic4 message.ui > ../gui/message.py
pyuic4 disk.ui > ../gui/disk.py
pyuic4 faq.ui > ../gui/faq.py
cd ../../../
