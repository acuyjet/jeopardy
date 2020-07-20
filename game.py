import requests

api_response = requests.get('https://jservice.io/api/random').json()
player_score = 0

# Prompt user for name
player_name = input("Hello! Please enter your name as you want it displayed on the monitor on the front of your podium: ")
print("\nThanks, {}! Let's play Jeopardy!".format(player_name))
print("\nRemember to phrase your response in the form of a question!\nEnter 'S' to skip a clue, and 'Q' at any time to quit.\n")

while True:
	# Display clue and prompt user for response
	print("{} for ${}: {}".format(api_response[0]['category']['title'].upper(), api_response[0]['value'], api_response[0]['question']))

	# If response is correct, add to score
	response = input()
	break


# If response is incorrect, subtract from score

# Allow user to break out of loop and answer Final Jeopardy clue

# Display total score and add to leaderboard
