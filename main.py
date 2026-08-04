import json

with open('media.json', 'r') as file:
    medialib = json.load(file)

moods = ["light", "serious", "funny", "sad", "exciting"]

def find_recommendations(media, mood, media_type, genre):
    recommendations = []

    for item in media:
        mood_matches = item["mood"] == mood
        type_matches = item["type"] == media_type
        genre_matches = not genre or genre in item["genres"].lower()

        if mood_matches and type_matches and genre_matches:
            recommendations.append(item)

    return recommendations

def main():

    print(f"Available moods: {moods}")
    print("Type 'exit' or 'quit' at any time to quit the program")

    while True:
        mood_input = input("What mood are you in? ").strip().lower()
        if mood_input in ['exit','quit']:
            break
        if mood_input not in moods:
            print("Choose one of the available moods ")
            continue
        type_input = input("Choose: 'movie' or 'show'? ").strip().lower()
        if type_input in ['exit','quit']:
            break
        if type_input not in ['movie', 'show']:
            print("Enter exactly 'movie' or 'show' ")
            continue
        genre_input = input("Enter a preferred genre, or press Enter to skip ").strip().lower()
        if genre_input in ['exit', 'quit']:
            break

        matches = find_recommendations(medialib, mood_input, type_input, genre_input)

        if matches:
            print("\nRecommendations:\n")

            for item in matches:
                print(f"Title: {item['title']}")
                print(f"Genres: {item['genres']}")
                print(f"Runtime: {item['runtime']}")
                print("-" * 40)
        else:
            print("Unfortunately a match was not found :(")

if __name__ == "__main__":
    main()