import requests

api_response = requests.get('https://jservice.io/api/random').json()
player_score = 0

# Prompt user for name
player_name = input("Hello! Please enter your name as you want it displayed on the monitor on the front of your podium: ")
print("\nThanks, {}! Let's play Jeopardy!".format(player_name))
print("\nRemember to phrase your response in the form of a question!\nEnter 'S' to skip a clue, and 'Q' at any time to quit.\n")

while True:
	# Display clue and prompt user for response
	response = input("{} for ${}: {}\n".format(api_response[0]['category']['title'].upper(
        ), api_response[0]['value'], api_response[0]['question']))

	if response.upper() == api_response[0]['answer'].upper():
		player_score += api_response[0]['value']
		print("Correct! You have ${}.".format(player_score))
	else:
		# If response is incorrect, subtract from score
		player_score -= api_response[0]['value']
		print("Oh, sorry! Incorrect. You have ${}.".format(player_score))
	
	# User can enter 'S' to skip a clue 
	# If response is correct, add to score

		# Allow user to break out of loop and answer Final Jeopardy clue
	if response.upper() == "Q":
		play_final = input(
			"Before you go, would you like to play Final Jeopardy? Y/N ")
		if play_final.upper() == "Y":
			if player_score <= 0:
				print("Sorry, you don't have enough to play, and you'll have to leave the stage in shame.")
				break
			final_wager = input(
				"How much would you like to wager? You have {}".format(player_score))
			response = input("{} for ${}: {}\n".format(api_response[0]['category']['title'].upper(
			), api_response[0]['value'], api_response[0]['question']))
			if response.upper() == api_response[0]['answer'].upper():
				player_score += final_wager
				print("Correct! Thanks for playing. Your final score is ${}.".format(player_score))
				break
			else:
				player_score -= final_wager
				print("Oh, sorry! Incorrect. Your final score is ${}.".format(player_score))
				break

	

# Display total score and add to leaderboard
