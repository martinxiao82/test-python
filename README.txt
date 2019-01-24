********* Before running the Python scripts *********
- Install pyserial by running in terminal:
pip install pyserial

- Install bluepy by running:
sudo apt-get install libglib2.0-dev
pip install bluepy

********* Running the tdb_interface.py script *********

Running the tdb_interface.py script by running:
sudo ./tdb_interface.py
OR
sudo python tdb_interface.py

********* Running the automated test script *********

1. Open sudoers file by running:
sudo gedit /etc/sudoers

2. Add "%sudo ALL=(ALL) NOPASSWD:ALL" to this file to run sudo commands without password

3. Put mcumgr inside "/trackr" folder

4. Run the automated test script by:
./test.py
OR
python test.py
