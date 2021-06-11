game = Minesweeper(4,4,3)
game.print()
AI = MinesweeperAI(4,4)

AI.add_knowledge((0,0),2)
AI.add_knowledge((0,1),2)
AI.add_knowledge((0,2),1)
AI.add_knowledge((2,1),3)

for s in AI.knowledge:
    print(s)

A = Sentence({(0,0),(1,1)},1)