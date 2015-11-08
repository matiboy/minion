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

Let's now add a command so Minion understands what to do with "say hi".


