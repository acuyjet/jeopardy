import re
import requests
import simpleaudio as sa

player_score = 0


def get_clue():
    api_response = requests.get('https://jservice.io/api/random').json()

    # If API returns 'None' for clue value or clue has an invalid_count, get another one
    if (api_response[0]['value'] == None) or (api_response[0]['invalid_count'] != None):
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


def play_think_music():
    think_music = 'think.wav'
    wave_obj = sa.WaveObject.from_wave_file(think_music)
    play_obj = wave_obj.play()


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

    # User can enter 'S' to skip a clue
    if response == 'S':
        print("\nThe correct response is {}. You have ${}.".format(
            clue[0]['answer'].upper(), player_score))

    # Allow user to break out of loop and answer Final Jeopardy clue
    if response == 'Q':
        play_final = input(
            "\nBefore you go, would you like to play Final Jeopardy? Y/N ")

        while play_final.upper() != 'Y' and play_final.upper() != 'N':
            play_final = input(
                "I'm sorry, I didn't get that. Would you like to play Final Jeopardy? Y/N ")

        if play_final.upper() == 'Y':

            if player_score <= 0:
                print(
                    "\nSorry, you don't have enough to play, and you'll have to leave the stage in shame.\n")
                break

            api_response = requests.get(
                'https://jservice.io/api/random').json()
            print("\nYour catgory is: {}".format(
                api_response[0]['category']['title']).upper())
            try:
                final_wager = int(input(
                    "\nHow much would you like to wager? You have ${}.\n> ".format(player_score)))
                while (final_wager > player_score) or (final_wager < 0):
                    final_wager = input(
                        "\nSorry, that's not a good bet. How much of your ${} would you like to wager?\n> ".format(player_score))
            except ValueError:
                print("Sorry, I didn't get that.")
                final_wager = int(input(
                    "\nHow much would you like to wager? You have ${}.\n> ".format(player_score)))
                while (final_wager > player_score) or (final_wager < 0):
                    final_wager = int(input(
                        "\nSorry, that's not a good bet. How much of your ${} would you like to wager?\n> ".format(player_score)))
            # Play a tune
            play_think_music()
            response = input("\n{}\n> ".format(
                api_response[0]['question'].upper()))

            # Clean up player response by removing the following: what, where, who, is, are, the, a, an, and, ?, &, whitespace
            clean_final_response = re.sub(
                r'(\bwhat\b|\bwhere\b|\bwho\b|\bis\b|\bare\b|\bwas\b|\bwere\b|\bthe\b|\ba\b|\ban\b|\band\b|[?&,\s])', '', response, 0, re.IGNORECASE)
            # Clean up answer by removing whitespace
            clean_final_answer = re.sub(
                r'([\s-])', '', api_response[0]['answer'], 0, re.IGNORECASE)

            if clean_final_response.upper() in clean_final_answer.upper():
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

    if form_of_question and response != 'S':
        # If yes, clean up player response by removing the following: what, where, who, is, are, the, a, an, and, ?, &, whitespace
        clean_response = re.sub(
            r'(\bwhat\b|\bwhere\b|\bwho\b|\bis\b|\bare\b|\bwas\b|\bwere\b|\bthe\b|\ba\b|\ban\b|\band\b|[?&,\s])', '', response, 0, re.IGNORECASE)
        # Clean up answer by removing whitespace
        clean_answer = re.sub(
            r'([\s-])', '', clue[0]['answer'], 0, re.IGNORECASE)

        # If both match, score as correct
        if clean_response.upper() in clean_answer.upper():
            player_score += clue[0]['value']
            print("\nCorrect! You have ${}.\n".format(player_score))

        # If don't match, score as incorrect
        elif response.upper() != clue[0]['answer'].upper() and response.upper() != 'S' and response.upper() != 'Q':
            player_score -= clue[0]['value']
            print('\nOh, sorry! The correct response is {}. You have ${}.\n'.format(
                clue[0]['answer'].upper(), player_score))

    # If no, score as incorrect
    if not form_of_question:
        player_score -= clue[0]['value']
        print('\nSorry, your response was not in the form of a question! The correct response is {}. You have ${}.\n'.format(
            clue[0]['answer'].upper(), player_score))
