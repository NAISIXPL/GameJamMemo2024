import arcade

from views.ViewManager import ViewManager

window = arcade.Window(1024, 768, "Meet IT")
manager = ViewManager(window)
manager.next()
arcade.run()
