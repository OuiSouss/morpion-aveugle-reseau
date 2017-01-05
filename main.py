
#!/usr/bin/env python3

from grid import *
import  random
from run import select_mode
import sys

def main(argv):
    #add function to select/create server/client
    select_mode(argv)

    """ grids est un tableau pour chaque vue
        grids[0] : vue observateur
        grids[1] : joueur numéro 1 premier connecté
        grids[2] : joueur numéro 2 deuxième connecté
    """
    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ?"))
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            grids[J1].display()
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !")
    else:
        print("you loose !")

if __name__ == "__main__":
    try:
        host = sys.argv[1]
    except IndexError:
        host = ""
    main(host)
    sys.exit(0)
