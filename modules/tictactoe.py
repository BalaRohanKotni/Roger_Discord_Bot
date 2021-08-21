from itertools import cycle


def format_row(row_num, one, two, three):
    row = 'ROW'
    return f'{row[row_num-1]+" "}{row_num} | {one} | {two} | {three} |'


def check_rows(bo):
    for i in range(3):
        counter = 0
        prev = ''
        for j in range(3):
            if prev == bo[i][j] and prev != ' ':
                counter += 1
            else:
                prev = bo[i][j]
        if counter == 2:
            return True


def check_cols(bo):
    for j in range(3):
        counter = 0
        prev = ''
        for i in range(3):
            if prev == bo[i][j] and prev != ' ':
                counter += 1
            else:
                prev = bo[i][j]
        if counter == 2:
            return True


def check_diagonals(bo):
    # check diagonal from left to right
    if bo[0][0] == bo[1][1] and bo[0][0] == bo[2][2] and bo[0][0] != ' ':
        return True
    # check diagonal from right to left
    if bo[0][2] == bo[1][1] and bo[0][2] == bo[2][0] and bo[0][2] != ' ':
        return True


# Create a board with no value


board = []


def reset_board():
    global board
    board = [[''*3]*3, [''*3]*3, [''*3]*3, ]

    for row in range(3):
        for column in range(3):
            board[row][column] = ' '


def format_board(bo):
    string = """
      C   O   L  
      1   2   3  
    -------------
"""

    for i in range(3):
        one = bo[i][0]
        two = bo[i][1]
        three = bo[i][2]

        string += format_row(i+1, one, two, three)+"\n"

        if i != 2:
            string += '    |' + '-'*3 + '+' + '-'*3 + '+' + '-'*3 + '|'+"\n"
    string += '    -------------'
    return string


async def gameplay(ctx, client, user):
    
    if user == client.user:
        await ctx.send("Sorry! Right now You can't play tictactoe with the bot.")
        return

    reset_board()

    players = ['X', 'O']
    player_cycle = cycle(players)

    channel = ctx.channel
    await ctx.send("Roger that! Creating a new tictactoe game.")

    curr_guild = client.guilds[client.guilds.index(channel.guild)]
    curr_channel = curr_guild.channels[curr_guild.channels.index(channel)]

    total_moves = 0

    prev_player = ''
    
    while True:

        if total_moves >= 9:
            await curr_channel.send("Game: Tie.")
            break

        if check_rows(board):
            await curr_channel.send('```{}```'.format(format_board(board)))
            await curr_channel.send("Game: {} won the game.".format(prev_player))
            break

        if check_cols(board):
            await curr_channel.send('```{}```'.format(format_board(board)))
            await curr_channel.send("Game: {} won the game.".format(prev_player))
            break

        if check_diagonals(board):
            await curr_channel.send('```{}```'.format(format_board(board)))
            await curr_channel.send("Game: {} won the game.".format(prev_player))
            break

        player = next(player_cycle)

        def get_move(m):
            return m.author == ctx.author or m.author == user

        await curr_channel.send('```'+format_board(board)+'\n\nTo make a move, use ROW,COL\nEx: To put to {} in the top left corner, use 1,1\n```'.format(player))

        await curr_channel.send("Game: {} make your move".format(player))

        while True:
            move = await client.wait_for('message', check=get_move)
            move = move.content

            if move == "q":
                await curr_channel.send("Game: {} ended the game.".format(player))
                return True
            try:
                row, col = move.split(',')
                if board[int(row)-1][int(col)-1] == ' ':
                    board[int(row)-1][int(col)-1] = player
                    total_moves += 1
                    break
                else:
                    await ctx.send("Game: Enter a valid choice.")
            except Exception as e:
                print("Tic tac toe exception:",e)
                await curr_channel.send("Game:Enter a valid choice")

        prev_player = player
    reset_board()
