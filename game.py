import requests

player_score = 0

# Prompt user for name
player_name = input(
    "Hello! Please enter your name as you want it displayed on the monitor on the front of your podium: ")
print("\nThanks, {}! Let's play Jeopardy!".format(player_name))
print("\nRemember to phrase your response in the form of a question!\nEnter 'S' to skip a clue, and 'Q' at any time to quit.\n")

while True:
    # Get clue
    api_response = requests.get('https://jservice.io/api/random').json()
    print("{} for ${}: {}\n".format(api_response[0]['category']['title'].upper(
    ), api_response[0]['value'], api_response[0]['question'].upper()))
    # Prompt user for response
    response = input("('S' to skip clue, 'Q' to quit) ")

    if response.upper() == api_response[0]['answer'].upper():
        # If response is correct, add to score
        player_score += api_response[0]['value']
        print("Correct! You have ${}.\n".format(player_score))
    # User can enter 'S' to skip a clue
    elif response.upper() == 'S':
        pass
    # Allow user to break out of loop and answer Final Jeopardy clue
    elif response.upper() == 'Q':
        break
    else:
        # If response is incorrect, subtract from score
        player_score -= api_response[0]['value']
        print('Oh, sorry! The correct response is "{}". You have ${}.\n'.format(api_response[0]['answer'], player_score))