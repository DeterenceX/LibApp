import requests

def fetch_book_info(isbn):
	
	url = f"https://openlibrary.org/isbn/{isbn}.json"
	try:
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		
		author_names = []
		if "authors" in data:
			for author_entry in data["authors"]:
				key = author_entry["key"]
				author_request = requests.get(f"https://openlibrary.org{key}.json")
				if author_request.status_code == 200:
					author_data = author_request.json()
					author_names.append(author_data.get("name", "unknown"))
						
		return {
			"isbn" : isbn,
			"title": data.get("title", "Unknown Title"),
			"author": " / ".join(author_names) if author_names else "unknown",
			"cover_url": f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg",
			"volume": None,
			"binding": None,
			"condition": None,
			"status": None,
			"rating": None
		}
	
	except Exception as e:
		print(f"Error fetching book info: {e}")
	return None
						
