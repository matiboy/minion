# Big Boss

## Getting started

### Install minimum requirements

```
$ pip install -r minimum_requirements.txt
```

### Fire it up
```
$ python bigboss.py
```

By default this uses the settings in `settings/boss.json`; you can run
```
$ BIGBOSS_SETTINGS=<path_to_your_settings_file> python bigboss.py
```
to override port and password settings

### Open web based interface

Point your browser to `http://localhost:5555`. Big boss uses basic auth to protect it from abuse. Use "admin" as login and "1" as password.

You can change the password in `settings/boss.json` or use an environment variable to point to another settings file.

### What should I see?

At this stage, you should see something like this:

![Empty big boss](https://cloud.githubusercontent.com/assets/487758/11019774/7775da8c-8643-11e5-885a-56ec7b5493eb.png)

## Where to from there?

### First step: nervous system

The first step is probably to set up a nervous system so your various components can communicate.

At the moment, only the Redis nervous system is available. So make sure to have a redis server running. Head over to nervous system and fill up the form with your environment details. If this is your first Minion instance, the host is probably `localhost` but when things get more interesting, it should be a shared resource.

### Add a sensor

Now you need your Minion instance to react to something. There are many [sensors](../minion/sensing) to read GPIO values, a HTTP(s) server, Infrared; but an easy start is to use a heartbeat which broadcasts a message at a fixed interval.

So head to Sensors, click "Add new" and in the form, under the class, select `minion.sensing.hearbeat.beat.Heartbeat`; leave the configuration to output a "say hi" message every 30 seconds. Click save.

### Make the Minion understand

Let's now add a command so Minion understands what to do with "say hi". Add a command component and choose the `minion.understanding.prefix.prefix.PrefixRemover` type and enter prefix: "say". Now Minion will listen to all commands starting with "say", remove that prefix and broadcast the rest of the message (in our case "hi") to the publish channel. You can see the publish channel under the Channels tab, it is `minion:do` (feel free to change it)

### Say it!

Finally, let's have an actuator speak out the message. Create an actuator, name it "Mouth" and choose type `minion.acting.mouth.macosx.say.SimpleSay` if on Mac, or `minion.acting.mouth.pyttsx.pyttsx.SimpleSay` if on Linux.

In the channels tab, let's make sure to have the `minion:do` channel as one of the entries, or the channel you picked for the "Say hi!" command output. Actuators can listen to several channels, just separate one per line in the textarea.

### Run it!
Finally, run 
```
$ python minion.py run --debug
```
to see (hear) the result


