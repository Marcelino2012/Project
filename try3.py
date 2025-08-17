import random 
print("hello")
print("1 = single player \n""2 = multi player")

player = ""
turn = 0
while player != "1" and player != "2":
    player = input("Enter your choice: ")
if player != "1" and player != "2":
    print(" You should enter 1 or 2 only")
board = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9] 
def print_board():
    print(board[0] , board[1] , board[2])
    print(board[3] , board[4] , board[5])
    print(board[6] , board[7] , board[8])
print_board()
print("player 1 is X player 2 is O")
def role():
    if board[0] == board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] == board[8]:
        return board[6]
    elif board[0] == board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] == board[8]:
        return board[2]
    elif board[0] == board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] == board[6]:
        return board[2]
    elif turn == 9:
        return "tie"


if player == "2":
    while True:
        print_board()
        if turn % 2 == 0:
            print("player 1 turn")
            x = int(input("inter your choice: ")) 
            if board[x - 1] in ("X" , "O"):
                print("choose another")
                continue 
            board[x - 1] = "X" 
        else:
            print("player 2 turn")
            y = int(input("inter your choice: ")) 
            if board[y - 1] in ("X", "O"):
                print("choose another")
                continue 
            board[y - 1] = "O"
        turn += 1  
        result = role()
        if result in ("X", "O", "tie"):
            break
 
            
result = role()
if result == "X":
    print("player 1 one win ")
elif result == "O":
    print("player 2 is win")
else:
    print("tie")
    
    
if player == "1":
    while True:
        print_board()
        if turn % 2 == 0:
            print("player 1 turn")
            x = int(input("inter your choice: ")) 
            if board[x - 1] in ("X" , "O"):
                print("choose another")
                continue 
            board[x - 1] = "X"
            turn += 1
        else:
            print("computer turn")
            empty = []
            for i in range(9):
                if board[i] not in ("X", "O"):
                 empty.append(i)
            z = random.choice(empty)
            board[z] = "O"
            turn += 1
        result = role()
        if result == "X":
            print("player 1 one win ")
            break
        elif result == "O":
            print("computer is win")
            break
        elif result == "tie":
            print("tie")
            break