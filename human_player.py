def play(game, player):
    print("Human Play")
    print(game)
    try:
        x, y = list(map(int, input().split()))
    except:
        print("Invalid input")
        return play(game, player)
    return x, y
