# for gnome, but also work with dunst

import sys
import gi
gi.require_version("Notify", "0.7")

from gi.repository import Notify

Notify.init("hello world")

Hello = Notify.Notification.new("Notif", "hi", "icon")

Hello.set_timeout(0) # doesn't dissapear until user moves mouse
Hello.show()








