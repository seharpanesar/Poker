from Game import Game
import pandas as pd
import os

iterations = 10
game = Game()

def main():

    all_data = []

    for i in range(iterations):
        raw_data = game.runGame()
        formatted_data = []

        for j, point in enumerate(raw_data):
            if j != len(raw_data)-1: # record player data
                best5String = [str(c) for c in point[1]]
                playerHandString = [str(c) for c in point[2]]

                formatted_data.extend([point[0], ", ".join(best5String), ", ".join(playerHandString)])
            else: # record common pool
                commonPoolString = [str(c) for c in point]
                formatted_data.append(", ".join(commonPoolString))

        all_data.append(formatted_data)

    dfColumns =[]

    dataTypes = ["Signal", "Best5Cards", "PlayerHand"]

    for i in range(6):
        for dataType in dataTypes:
            dfColumns.append("{}P{}".format(dataType, i+1))

    dfColumns.append("commonPool")

    df = pd.DataFrame(all_data, columns=dfColumns)

    df.to_csv(os.getcwd()+"\\..\\poker_data.csv", index=False)

if __name__ == "__main__":
    main()