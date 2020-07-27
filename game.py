import requests

player_score = 0


def get_clue():
    api_response = requests.get('https://jservice.io/api/random').json()

    # If API returns 'None' for clue value, get another one
    if api_response[0]['value'] == None:
        api_response = requests.get('https://jservice.io/api/random').json()
    print("\n{} for ${}: {}\n".format(api_response[0]['category']['title'].upper(
    ), api_response[0]['value'], api_response[0]['question'].upper()))

    return api_response


# Check to make sure response is in the form of a question
def is_question(response):
    if (response.find("WHAT")) != -1 or (response.find("WHERE")) != -1 or (response.find("WHO")) != -1:
        return True
    elif (response == 'S') or (response == 'Q'):
        return True
    else:
        return False


# Prompt user for name
player_name = input(
    "Hello! Please enter your name as you want it displayed on the monitor on the front of your podium: ")
print("\nThanks, {}! Let's play Jeopardy!".format(player_name))
print("\nRemember to phrase your response in the form of a question!\nEnter 'S' to skip a clue, and 'Q' at any time to quit.\n")

while True:

    # Get clue
    clue = get_clue()

    # Prompt user for response
    response = input("('S' to skip clue, 'Q' to quit)\n> ").upper()

    form_of_question = is_question(response)

    if form_of_question:
        # If yes, strip out question word and compare to ['answer']
        # If response matches, score as correct
        if response.upper() == clue[0]['answer'].upper():
            player_score += clue[0]['value']
            print("\nCorrect! You have ${}.\n".format(player_score))

        # If response doesn't match, score as incorrect
        elif response.upper() != clue[0]['answer'].upper() and response.upper() != 'S' and response.upper() != 'Q':
            player_score -= clue[0]['value']
            print('\nOh, sorry! The correct response is {}. You have ${}.\n'.format(
                clue[0]['answer'].upper(), player_score))
    # If no, score as incorrect
    else:
        player_score -= clue[0]['value']
        print('\nSorry, your response was not in the form of a question! The correct response is {}. You have ${}.\n'.format(
            clue[0]['answer'].upper(), player_score))

    # If response is incorrect, subtract from score

    # User can enter 'S' to skip a clue
    if response == 'S':
        print("\nThe correct response is {}. You have ${}.".format(
            clue[0]['answer'].upper(), player_score))
        pass

    # Allow user to break out of loop and answer Final Jeopardy clue
    elif response == 'Q':
        play_final = input(
            "\nBefore you go, would you like to play Final Jeopardy? Y/N ")

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
            response = input("\n{}\n\n(doo doo doo doo-doo doo doo doo ...)\n> ".format(
                api_response[0]['question'].upper()))

            if response.upper() == api_response[0]['answer'].upper():
                player_score += final_wager
                print("\nCorrect! Thanks for playing. Your final score is ${}.".format(
                    player_score))
                break

            else:
                player_score -= final_wager
                print("\nOh, sorry! That's incorrect. The correct response is {}. Your final score is ${}.".format(
                    api_response[0]['answer'].upper(), player_score))
                break

        elif play_final.upper() == 'N':
            print("\nThanks for playing! Your final score is ${}.\n".format(
                player_score))
            break
