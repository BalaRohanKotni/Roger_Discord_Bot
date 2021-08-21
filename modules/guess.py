import random


async def _guess(ctx, client):

    command_caller = ctx.author

    await ctx.send("Guess a number between **1** and **10** || Type 0 to exit")
    r = random.randint(1, 10)
    print(r)
    while True:

        def check_guess(m):
            return m.author == command_caller

        guess = await client.wait_for('message', check=check_guess)

        user = guess.author
        guess = guess.content
        print(guess)

        try:
            if int(guess) < 0 or int(guess) > 10:
                await ctx.send("Guess within the range.")
            else:
                if int(guess) == 0:
                    await ctx.send("You aborted the guess!")
                    break
                elif int(guess) == r:
                    await ctx.send("You got it right! 😀 Congratulations! {}".format(user.mention))
                    break
                elif int(guess) > r:
                    await ctx.send("Try a little low! Try again. 😞")
                elif int(guess) < r:
                    await ctx.send("Try a little higher! Try again. 😞")
        except Exception as e:
            print(e)
            await ctx.send("Only numbers are allowed! Try again. 😞")
