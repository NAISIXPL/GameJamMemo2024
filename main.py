import arcade

from views.GameView import GameView

window = arcade.Window(1024, 768, "Meet IT")
view = GameView("./assets/tile_map.json", "POLICJA")
window.show_view(view)
arcade.run()
