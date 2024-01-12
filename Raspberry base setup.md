Using "Imager" installing Raspi OS 64bit Desktop on the SD card.
Booting up Raspi Zero 2, following the instructions setting up the OS for use.
At the first start, start the Terminal application.
Conforming version number:
Run the commands:
  -cat /etc/os-release
    PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
    ...
Check for updates:
  -sudo apt update
  -sudo apt upgrade
In the settings menu Raspberry Pi Configuration or from terminal by command "sudo raspi-config" enable SSH if necessarly.
In the Display turn off Screen Blanking. (Also optional)
