import requests

player_score = 10

# Prompt user for name
player_name = input(
    "Hello! Please enter your name as you want it displayed on the monitor on the front of your podium: ")
print("\nThanks, {}! Let's play Jeopardy!".format(player_name))
print("\nRemember to phrase your response in the form of a question!\nEnter 'S' to skip a clue, and 'Q' at any time to quit.\n")

while True:
    # Get clue
    api_response = requests.get('https://jservice.io/api/random').json()
    # If API returns 'None' for clue value, get another clue
    if api_response[0]['value'] == None:
        api_response = requests.get('https://jservice.io/api/random').json()
    print("\n{} for ${}: {}\n".format(api_response[0]['category']['title'].upper(
    ), api_response[0]['value'], api_response[0]['question'].upper()))
    # Prompt user for response
    response = input("('S' to skip clue, 'Q' to quit)\n> ")

    if response.upper() == api_response[0]['answer'].upper():
        # If response is correct, add to score
        player_score += api_response[0]['value']
        print("\nCorrect! You have ${}.\n".format(player_score))
    # User can enter 'S' to skip a clue
    elif response.upper() == 'S':
        print("The correct response is {}. You have ${}.".format(
            api_response[0]['answer'].upper(), player_score))
        pass
    # Allow user to break out of loop and answer Final Jeopardy clue
    elif response.upper() == 'Q':
        play_final = input(
            "Before you go, would you like to play Final Jeopardy? Y/N ")
        while play_final.upper() != 'Y' and play_final.upper() != 'N':
            play_final = input(
                "\nI'm sorry, I didn't get that. Would you like to play Final Jeopardy? Y/N ")
        if play_final.upper() == 'Y':
            if player_score <= 0:
                print(
                    "\nSorry, you don't have enough to play, and you'll have to leave the stage in shame.\n")
                break
            api_response = requests.get(
                'https://jservice.io/api/random').json()
            print("\nYour catgory is: {}".format(
                api_response[0]['category']['title']).upper())
            final_wager = int(
                input("\nHow much would you like to wager? You have ${}. ".format(player_score)))
            response = input("\n{}\n(doo doo doo doo-doo doo doo doo ...)\n> ".format(
                api_response[0]['question'].upper()))
            if response.upper() == api_response[0]['answer'].upper():
                player_score += final_wager
                print("\nCorrect! Thanks for playing. Your final score is ${}.".format(
                    player_score))
                break
            else:
                player_score -= final_wager
                print("Oh, sorry! That's incorrect. The correct response is {}. Your final score is ${}.".format(
                    api_response[0]['answer'].upper(), player_score))
                break
        elif play_final.upper() == 'N':
            print("\nThanks for playing! Your final score is ${}.\n".format(
                player_score))
            break
    else:
        # If response is incorrect, subtract from score
        try:
            player_score -= api_response[0]['value']
            print('\nOh, sorry! The correct response is {}. You have ${}.\n'.format(
                api_response[0]['answer'].upper(), player_score))
        # If API returns 'None' for clue value, catch TypeError
        except TypeError:
            print("Whoops, the writers made an error. Let's try another clue.")
