Title: How to couple a service to a USB device
date: 2014-01-24 23:30
Category: blog
Tags: squeezebox, music, osx, usb, launchd, service, udev

I am a music junkie, and so is my wife. We are both heavy users of Logitech's [Squeezebox](http://en.wikipedia.org/wiki/Logitech_Media_Server) system. Even though Logitech doesn't distribute *hardware* devices any more, Squeezebox  always was, and still is, a great -- free and open source -- *software* solution for those of us who want to

* have all of their music stored in a central place,
* listen to it on devices for pretty much any platform (Linux, Mac, Windows, Android, iOS),
* control each player with the named devices, plus a browser frontend,
* synchronize playback over groups of players (party music in living room, kitchen, and garden),
* add other sources via plugins (internet radio, Last FM, Pandora, Spotify, ...).

The core of this ecosystem in my household is a Mac mini in my living room which serves my music -- organized with iTunes -- with the Logitech Media Server software. At the same time, I take advantage of Triode's awesome [squeezelite](https://code.google.com/p/squeezelite/) player in order to turn my Mac mini into a headless player which I control either via the server's web interface or with an app on my smartphone or tablet. The Mac mini is coupled to my amplifier by means of an audiophile USB DAC.

And here is the problem which I ran into: When the squeezelite player software is started, you can choose the sound device you want to route the audio output to. The audio device has to be active when the squeezelite instance is fired up, and it has to stay active. But my USB DAC is only turned on when I want to listen to music. The problem boils down to a fairly general question:

###The abstract problem###

>How can one couple a service to a USB device, that is start (stop) a service when the device is plugged in (out)?

In the Linux world, the generic answer is "set up a [udev](http://en.wikipedia.org/wiki/Udev) rule". In OS X, things aren't that straightforward: in the year 2010, I spent a fair amount of time scanning the internet for a solution to this -- apparently -- standard problem. At that time, I wasn't able to find a solution which required only configuration, no coding.

* I did find an Apple [snippet](https://developer.apple.com/library/mac/samplecode/USBPrivateDataSample/Listings/USBPrivateDataSample_c.html) of C code. My modified [version](http://forums.slimdevices.com/showthread.php?83994-SqueezeSlave-External-USB-audio-interface-%28Mac-OS-X%29) appears to work fine. I do not understand too much of `CoreFoundation` programming, though, which is why I'm shy to post the solution here, but maybe I'll do someday.
* A little later I became aware of a more user friendly alternative which takes advantage of the free context manager [ControlPlane](http://www.controlplaneapp.com/). I used it for quite some time. Actually, I was going to write this very post to explain how to set it up.
* When I started to write this article, I googled again and became aware of another recently posted [solution](http://stackoverflow.com/questions/7240117/execute-an-application-on-mac-os-x-when-a-particular-type-of-usb-device-is-conne) which uses only `launchd`. I decided to explain this solution instead of the ControlPlane variant.

###Writing a service wrapper###

As a prerequisite for any of the aforementioned variants, we need to wrap the `squeezelite` executable as a service. How to accomplish this is of interest in its own right. First, create a folder to host the service wrapper:

``` sh
$ md '/Library/Application Support/squeezelite/'
```

Now, run the following command:

``` sh
$ squeezelite -l
Output devices:
  1 - Built-in Output [Core Audio]
  2 - C-Media USB Headphone Set   [Core Audio]
```

It shows the available output devices of your computer. My external USB DAC has the device number 2. Make the script executable and test whether it works correctly (you can stop the `squeezelite` process with `Ctrl-C`):

```sh
$ /usr/local/bin/squeezelite -o 2 -m 00:00:00:00:00:02
```

The `-m` option sets a dummy MAC which should be unique for each player instance. This allows the Logitech Media Server to save the player state over disconnects or restarts. Set up a file `squeezelite.n.plist` for each relevant output device `n`:

<div data-gist-id="8608886" data-gist-file="squeezelite.n.plist"></div>

It specifies a `launchd` service `squeezelite-n` which keeps alive an instance of the process launched by the command

``` sh
$ /usr/local/bin/squeezelite -o n -m 00:00:00:00:00:0n
```

In my case, there would be one file `squeezelite.2.plist`. Test whether the service starts ...

``` sh
$ launchctl load '/Library/Application Support/squeezelite/squeezelite.2.plist'
$ launchctl list | grep squeezelite
13854   -   0x7fe4d0c6e8f0.anonymous.squeezelite
13850   -   squeezelite-2
$ ps -A | grep squeezelite | grep -v grep 
13854 ??         0:00.28 /usr/local/bin/squeezelite -o 2 -m 00
```

... and stops correctly:

``` sh
$ launchctl unload '/Library/Application Support/squeezelite/squeezelite.2.plist'
$ launchctl list | grep squeezelite
$ ps -A | grep squeezelite | grep -v grep 
```

###Couple the service launch to a USB event###

That's it for the `launchd` service wrapper. Now you have to couple the launch of this service to the attachment of a USB device. To that end, add the following key-value pairs to the `dict` of `squeezelite.n.plist`

``` xml
<key>LaunchEvents</key>
<dict>
  <key>com.apple.iokit.matching</key>
  <dict>
    <key>com.apple.device-attach</key>
    <dict>
      <key>idProduct</key>
      <integer>...</integer>
      <key>idVendor</key>
      <integer>...</integer>
      <key>IOProviderClass</key>
      <string>IOUSBDevice</string>
      <key>IOMatchStream</key>
      <true/>
    </dict>
  </dict>
</dict>
```

Find out product and vendor ID of the USB device in question:

``` sh
$ system_profiler SPUSBDataType
USB:
    [...]

        C-Media USB Headphone Set  :

          Product ID: 0x000c
          Vendor ID: 0x0d8c  (C-MEDIA ELECTRONICS INC.)
    [...]
```

In my case, the product ID would be 12 and the vendor ID would be 3468. This is my complete file:

<div data-gist-id="8608886" data-gist-file="squeezelite.2.plist"></div>

Now, load the service again and use `ps -A` to convince yourself that `squeezelite` is only running when the USB device is connected. If you wish to load the service at boot time, you should write-protect the service definition and then link it to `/Library/LaunchDaemons':

``` sh
$ sudo chown -R root:wheel '/Library/Application Support/squeezelite/'
$ sudo chmod 644 '/Library/Application Support/squeezelite/squeezelite.2.plist'
$ sudo ln -s '/Library/Application Support/squeezelite/squeezelite.2.plist' /Library/LaunchDaemons
```

Reboot and have fun!