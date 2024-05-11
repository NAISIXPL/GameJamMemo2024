import arcade

from views.GameView import GameView

window = arcade.Window(1024, 768, "Meet IT")
view = GameView()
window.show_view(view)
arcade.run()
