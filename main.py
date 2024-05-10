import arcade

from views.GameView import GameView

window = arcade.Window(800, 600, "Meet IT")
view = GameView()
window.show_view(view)
arcade.run()
