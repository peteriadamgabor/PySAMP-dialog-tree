from python.job.rout import Rout
from python.player.player import Player


def rout_create_handler(player: Player, r: float):

    (x, y, z) = player.get_pos()
    player.set_checkpoint(x, y, z, r)
    player.check_points.append(Rout(x, y, z, r))

