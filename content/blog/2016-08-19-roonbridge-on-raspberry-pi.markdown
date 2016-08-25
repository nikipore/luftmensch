Title: RoonBridge on Raspberry Pi
date: 2016-08-19 23:00
Category: blog
Tags: roon, music, raspberry-pi, hifiberry

Long time no see ... did I mention that [I am a music junkie and Squeezebox fan]({filename}2014-01-24-couple-service-to-usb-device.markdown)? Well, last time my Mom was here, she became a fan, too, and asked me to set that up at her place. Problem is, Logitech doesn't build hardware any more, so Mom'll have to become a user of modded hardware, and this in view of the inequality _MAF_ ≤ _WAF_, were the two quantities represent the Mom and Wife Acceptance Factor, respectively.

Although I still own a Squeezebox Radio and a Touch, all serious players are squeezelite clients running on Macs and Raspberry Pis with HifiBerry DAC+ sound cards or external DACs and therefore in geek territory. For the Pis, I use the [piCorePlayer](https://sites.google.com/site/picoreplayer/home) distribution which is foolproof because it is specialized on running a squeezelite client and runs in read-only mode; after booting it doesn't require the SD card any more, so you can power off simply by unplugging it from the wall outlet. With such a setup, the chances that my Mom (in her 70s and 200 kms away) needs my support because anything becomes inconsistent are greatly diminished.

Modding always pushes my geek and gearhead buttons, so I reconsidered my current solution and came across [Roon](https://roonlabs.com/) which since release 1.2 comes with RoonBridge, an audio endpoint for standard hardware (Mac, Windows, and Linux) and hence for the whole spectrum of audio hardware; you could call it squeezelite for Roon. I got hooked immediately and started to experiment with my living room Mac mini which hosts the music (as before), runs the Roon core (instead of Logitech Media Server) and a bridge (instead of squeezelite) plus one Raspberry Pi 3 with HiFiBerry DAC+ as prototype endpoint for the other rooms. You don't leave a marvelous, free, and long-term stable solution like the Squeezebox ecosystem lightly, but in the end I shelled out the $500 for a Roon lifetime membership with pleasure and said farewell to Squeezebox — unless my Mom would be needing my support, that is. In fact, she'll stay outside geek territory because she can now get away with my retired Logitech hardware.

The list of requirements for my new setup reads as follows:

* Built from scratch by myself.
* Based upon a standard and small Linux distribution, ideally a Debian derivative which supports onboard, external Wi-Fi, and HiFiBerry DAC+ support out-of-the-box (no self-compiled kernels).
* Very simple to set up and maintain, tolerant against hard power on and off.
* This implies an SD card friendly setup with read-only or "mostly" read-only mode.
* Works as audio endpoint for the following protocols: Roon (must), AirPlay (must), Chromecast (nice-to-have), Bluetooth (nice-to-have)

###Install Raspbian Lite###

[Raspbian Lite](https://downloads.raspberrypi.org/raspbian_lite_latest) is my choice. It's a slimmed down Debian Jessie with all the drivers for the Raspberry Pi 3 onboard hardware (Wi-Fi, Bluetooth) and the most important extensions including the HiFiBerry DAC+. Download it and burn it to an SD card. Any class 10 card with 2 GB will do, 4 GB leaves plenty of room for extensions. Take a small card if you plan to clone it to other cards later on, because growing partitions larger is easy, while shrinking them is a bit tricky. I often use [Etcher](https://www.etcher.io/) on OS X, but this is how you do this without additional tools:

``` sh
~ diskutil list # find your SD card and note its disk number <n>
~ diskutil unmountDisk disk<n>
~ sudo dd bs=1m if=~/Downloads/raspbian-jessie-lite.img of=/dev/rdisk<n>
~ diskutil eject disk<n>
```

The `r` in `rdisk` stands for "raw device" and accelerates the copy process greatly. Plug the SD card into the Raspberry Pi and boot. Find out the IP address or hostname (referred to as `<host>` in what follows) of the Pi and login via SSH as `pi` with password `raspberry`.

###SSH without password (config)###

I make a short excursion here because I prefer to login without password, so the optional steps are to put your public key on the Pi:
``` sh
~ scp .ssh/id_rsa.pub pi@<host>:~
~ ssh pi@<host>
$ mkdir .ssh && chmod 700 .ssh
$ cat id_rsa.pub >> .ssh/authorized_keys && rm id_rsa.pub && chmod 600 .ssh/authorized_keys
```

Edit `/etc/ssh/sshd_config`, find and change the `PasswordAuthentication` option to `no`,
``` sh
$ sudo vi /etc/ssh/sshd_config
[...]
PasswordAuthentication no
[...]
```

then restart the `ssh` service:
``` sh
$ sudo service ssh restart
```

Beware: Before closing the SSH session, check if you still are able to log in by opening another session.

###Time Zone###

If you wish to have your local time shown correctly, you have to set it as follows (replace `Europe/Berlin` with your time zone):
```sh
$ sudo rm /etc/localtime && sudo ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime
```

###Host Name###

Time to set up the host name. It should be something mnemonic; I'll use `roonbridge` for now. The first step should be to assign the host name on your router server (if it allows to set host names based on the MAC address), so connecting via `ssh` is a lot easier. The second step is to have the Pi itself infer it correctly, because the result of the command `hostname` is shown in Roon Control and also in the AirPlay device name.

If you prefer to set the host name to a static value:
```
$ sudo su -
$ echo roonbridge > /etc/hostname
$ exit
```

Alternatively, if you wish to obtain your [hostname dynamically via DHCP](http://blog.schlomo.schapiro.org/2013/11/setting-hostname-from-dhcp-in-debian.html
):
```
$ sudo su -
$ echo localhost > /etc/hostname
$ echo unset old_host_name > /etc/dhcp/dhclient-enter-hooks.d/unset_old_hostname
$ exit
```

I usually choose the first option (static) because I find that the services of the Roon and AirPlay endpoints start up so early that the host hasn't obtained a DHCP lease and DNS entry yet so the corresponding services will show `localhost` unless they are restarted explicitly. I could probably look deeper into the details of the service startup dependencies, but I don't feel it is worth the trouble.

###Setup Wi-Fi###

I recommend not to use Wi-Fi for high resolution audio playback when you can avoid it. Although Roon is very graceful because the clocking takes place in the endpoint, Wi-Fi is often brittle. But if you cannot do without Wi-Fi (which I cannot in my bathroom), [here](http://www.christeck.de/wp/2016/03/25/raspberry-pi-3-networking-issues/) is how to set that up. Scan for wireless networks:

``` sh
$ iwlist wlan0 scan
```

Add the following at the end of the file `/etc/wpa_supplicant/wpa_supplicant.conf`:

``` sh
$ sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
[...]
network={
    ssid="<ESSID>"
    psk="<your password>"
}
```

At this point, `wpa-supplicant` will normally notice a change has occurred within a few seconds, and it will try and connect to the network. If it does not, manually restart the interface with

``` sh
$ sudo ifdown wlan0 && sudo ifup wlan0
```

You can verify if it has successfully connected calling
``` sh
$ ifconfig wlan0
```

If the `inet addr` field has an address beside it, the Pi has connected to the network. If not, check that your password and ESSID are correct.

###External Wi-Fi Adapter###

In the bathroom, the onboard Wi-Fi reception is so weak that I had to resort to an external Wi-Fi Adapter (TP-Link TL-WN822N). Running `ifconfig`, it shows up as `wlan1`, so deactivate onboard Wi-Fi which will free the `wlan0` device in favor of the external Wi-Fi adapter upon reboot:
``` sh
$ sudo vi /etc/modprobe.d/disable-onboard-wifi.conf
blacklist brcmfmac
blacklist brcmutil
$ sudo reboot
```

###Disable Onboard Bluetooth###

You might also have wanted to disable onboard Wi-Fi in order to reduce power consumption and radiation, so here is how to disable Bluetooth as well:
``` sh
$ sudo vi /etc/modprobe.d/disable-bluetooth.conf
blacklist btbcm
blacklist hci_uart
$ sudo reboot
```

###HiFiBerry DAC+###

If you have a HifiBerry DAC+ card on top of your Raspberry 3 (like I do), you probably want to [disable the onboard sound card and enable the HifiBerry](http://pi.bek.no/HiFiBerry/) by editing `/boot/config.txt`,
``` sh
$ sudo vi /boot/config.txt
```

commenting out this line
``` sh
#dtparam=audio=on
```

and adding the line
``` sh
dtoverlay=hifiberry-dacplus
```

Restart the Pi and test that you indeed see the HiFiBerry (and only it):
``` sh
$ sudo reboot
$ aplay -l # note the card number; should be 0
```

Now, [configure ALSA](https://www.hifiberry.com/guides/mixer-settings/) by creating `/etc/asound.cnf`:
```
$ sudo vi /etc/asound.cnf
pcm.!default {
    type hw
    card 0
}

ctl.!default {
    type hw
    card 0
}
```

###SD Card Friendliness###

Besides its plug & play simplicity and support of all relevant sound cards (including HiFiBerries), the biggest advantage of piCorePlayer is its read-only mode. But I find [Tiny Core Linux](http://wiki.tinycorelinux.net/) not straightforward when it comes to arbitrary 3rd party software (like RoonBridge) or complex setups with external Wi-Fi, Bluetooth, etc. So, how do we get something which approximates hard read-only mode sufficiently well in the sense that the risk of corrupting your SD card is strongly mitigated? Answer (adapted from [here](https://pi-buch.info/raspbian-lite-fuer-den-read-only-betrieb-konfigurieren/
)):

1. Disable swapping,
2. mount the boot partition as read-only, and
3. mount `/tmp` and `/var/log` as RAM disks.

First, disable swapping:
``` sh
$ sudo su -
$ service dphys-swapfile stop
$ systemctl disable dphys-swapfile
$ rm /var/swap
```

You also have to change `/boot/cmdline.txt`. At the end of the long line of options append the options `fastboot noswap` hinzu. `fastboot` means that no file system check should be performed during boot. `noswap` means, well, don't swap.
``` sh
$ sudo vi /boot/cmdline.txt
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait fastboot noswap
```

The last line shows how it looks on my system, your mileage may vary. You have to make two changes to `/etc/fstab`:

1. Mount `/boot` as read-only (option `ro`).
2. Add two lines to mount `/var/log` und `/tmp` as `tmpfs`.

``` sh
$ sudo vi /etc/fstab
proc            /proc                      proc    defaults          0 0
/dev/mmcblk0p1  /boot                      vfat    ro,defaults       0 2
/dev/mmcblk0p2  /                          ext4    defaults,noatime  0 1
tmpfs           /var/log                   tmpfs   nodev,nosuid      0 0
tmpfs           /tmp                       tmpfs   nodev,nosuid      0 0
```

Again, this is how my `/etc/fstab` looks like, yours may differ. Now reboot 
``` sh
$ sudo reboot
```

and test whether everything works as announced:
``` sh
$ mount | grep mmcblk
$ sudo touch /boot/xy
touch: cannot touch ‘/boot/xy’: Read-only file system
```

###Update###

If you ever want to update your kernel or firmware, you'll need to remount `/boot` in `rw` mode, so here is the procedure:

``` sh
$ sudo su -
$ mount -o remount,rw /boot
$ apt-get update && apt-get -y dist-upgrade
$ apt-get -y install rpi-update
$ rpi-update
$ reboot
```

Now, the Pi will come back up with `/boot` again mounted in `ro` mode.

###RoonBridge###

Simply follow the [instructions](https://kb.roonlabs.com/LinuxInstall) (I didn't have to install any dependencies):
``` sh
$ curl -O http://download.roonlabs.com/builds/roonbridge-installer-linuxarmv7hf.sh
$ chmod +x roonbridge-installer-linuxarmv7hf.sh
$ sudo ./roonbridge-installer-linuxarmv7hf.sh
$ rm roonbridge-installer-linuxarmv7hf.sh
```

Now test whether the new bridge shows up as `snd_rpi_hifiberry_dacplus` in Roon Control's audio settings. If everything is ok, you should move Roon's logs to the RAM disk:

``` sh
$ sudo su -
$ rm -r /var/roon/RAATServer/Logs && ln -s /var/log /var/roon/RAATServer/Logs
$ rm -r /var/roon/RoonBridge/Logs && ln -s /var/log /var/roon/RoonBridge/Logs
```

In order to avoid that your RAM disk runs full, you should point `logrotate` at the logs. To that end, create a config file `/etc/logrotate.d/roon` with the following content:
``` sh
$ sudo vi /etc/logrotate.d/roon
/var/roon/RoonBridge/Logs/RoonBridge_log.txt
/var/roon/RAATServer/Logs/RAATServer_log.txt
{
    rotate 7
    daily
    missingok
    notifempty
    copytruncate
    delaycompress
    compress
}
```

###AirPlay###

I find it very nice to have other endpoints besides the RoonBridge, the most relevant being AirPlay. Chromecast seems to be possible but is not on top of my list. Bluetooth has lower quality, is fiddly to set up and therefore has low priority for me, but AirPlay has CD quality, its implementation [Shairport Sync](https://github.com/mikebrady/shairport-sync) is straightforward to set up and works nicely side by side with the RoonBridge; both claim exclusive control of the sound card before playing and release control when they are done.

Since there is only a Debian 9 (Stretch) package, and Raspbian Lite is Debian 8 (Jessie) at the time of writing, you have to roll your own. Don't worry, it's simple and straightforward. Just follow the instructions at the [GitHub site](https://github.com/mikebrady/shairport-sync):
``` sh
$ sudo apt-get install -y build-essential git autoconf automake libtool libdaemon-dev libasound2-dev libpopt-dev libconfig-dev avahi-daemon libavahi-client-dev libssl-dev libsoxr-dev
$ mkdir git && cd git
$ git clone https://github.com/mikebrady/shairport-sync.git
$ cd shairport-sync && autoreconf -i -f
$ ./configure --with-alsa --with-avahi --with-ssl=openssl --with-soxr --with-systemd
$ make
$ getent group shairport-sync &>/dev/null || sudo groupadd -r shairport-sync >/dev/null
$ getent passwd shairport-sync &> /dev/null || sudo useradd -r -M -g shairport-sync -s /usr/bin/nologin -G audio shairport-sync >/dev/null
$ sudo make install
```

Now create `/etc/shairport-sync.conf` with the following content:
``` sh
$ sudo vi /etc/shairport-sync.conf
general =
{
    name = "%h";
};

alsa =
{
    output_device = "hw:0";
    mixer_control_name = "Digital";
};
```

You'll have to infer the mixer name from `alsamixer`; `Digital` is the correct name for the HifiBerry DAC+. The device is `hw:0` because we deactivated onboard sound, otherwise it would have been `hw:1`. Now start the service
``` sh
$ sudo systemctl enable shairport-sync
```

and test it from an iOS device.

###SD Card Backup###

Now you have a shiny new SD card image which you can backup and reuse for other Raspberry Pis — I've got 5, most of them identical, save the external Wi-Fi stuff for my bathroom endpoint and an external DAC/AMP for my headphone endpoint. The steps to remove `.bash_history` and `.lesshst` are optional, but the cleanup of the Roon data isn't. Roon generates unique IDs at first startup and will not be able to tell the clones apart from the master:
``` sh
$ sudo su -
$ rm -r /var/roon/*/* && ln -s /var/log /var/roon/RAATServer/Logs && ln -s /var/log /var/roon/RoonBridge/Logs
$ rm ~pi/.lesshst
$ rm ~pi/.bash_history
$ rm ~/.lesshst
$ rm ~/.bash_history
$ shutdown -h now
```

Remove the SD card from the Pi and insert it into an SD card reader attached to your your Mac (there are instructions for Windows and Linux all over the web):
``` sh
~ diskutil list
~ diskutil unmountDisk disk<n>
~ sudo dd bs=1m if=/dev/rdisk<n> of=~/Desktop/raspbian-lite-roonbridge.img
~ diskutil eject disk<n>
```

###Use SD card on another Pi###

Burn your backup image as described above. In order to avoid to have to shrink the image, it makes sense to use a larger card. Insert the SD card into your Pi and power it up. Give it a host name as described above. Then expand the root partition to the entire size of the card:
``` sh
$ sudo su -
$ echo your-host-name > /etc/hostname
$ raspi-config # choose "expand_rootfs"
$ reboot
```

That's it. Really, very simple.

###Shrink Root Partition###

If you weren't able to burn your master image to another SD card because the target SD card is too small, you have to shrink the master's root partition. You can run into this situation even when the source and target SD cards are apparently identical (same make and model) — I did.

While expanding is straightforward and risk-free on a running Pi (we did it using `raspi-config` a few lines above), shrinking isn't. I find the safest and easiest way to use a [GParted Live CD](http://gparted.org/livecd.php) which you can boot directly from the image with a VM software like [VirtualBox](https://www.virtualbox.org/). Just download the i686 version, create a new generic "Linux 32-bit" virtual machine, and select the downloaded image. After booting the Live CD, plug the (too large) source SD card into the host compuer, associate the USB device with the VM, and resize the root partition as you like. GParted essentially performs two operations:

1. It applies `resize2fs` which moves the file system in the partition into a contiguous space of the target size which renders the tail of the partition vacant.
2. It truncates the tail of the partition s.t. the partition size equals the new file system size.

Et voilà, if you are using 4 GB cards, you are a happy owner of a 4–ε GB master image which should fit any clone. I also tried the more elegant approach to apply this operation directly to an image of the card (as opposed to the card itself) mounting that image with `diskutil` and acquainting it with the GParted VM, but to no avail; I didn't persist too much, though.

###USB DAC###

Add the following line to `/etc/modprobe.d/alsa-base.conf`:
``` sh
$ sudo vi /etc/modprobe.d/alsa-base.conf
options snd-usb-audio index=0
```

With this setting, the USB DAC should acquire the hardware card number `0`, and `/etc/asound.cnf` should work as described above. The mixer name in `/etc/shairport.sync` has to be set to the value displayed in `alsamixer`, e.g.
``` sh
$ sudo vi /etc/shairport-sync.conf
[...]
alsa =
{
    output_device = "hw:0";
    mixer_control_name = "PCM";
};
```

###To Do###

- Bluetooth audio (both TX and RX)
