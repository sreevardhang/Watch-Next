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

def find_title(medialist, usertitle):
    cleantitle = usertitle.strip().lower()

    for item in medialist:
        if cleantitle in item['title'].lower():
            return item

    return None

def calculate_score(selectedtitle, medialist):
    scores = {}

    medialist = (item for item in medialist if selectedtitle['title'] not in item['title'])

    selected_genres = set(genre.strip().lower() for genre in selectedtitle['genres'].split(','))

    for item in medialist:
        if selectedtitle['title'] in item['title']:
            continue

        item_score = 0

        if selectedtitle['mood'] == item['mood']:
            item_score += 3

        if selectedtitle['type'] == item['type']:
            item_score += 1

        item_genres = set(genre.strip().lower() for genre in item['genres'].split(','))

        shared_genres = selected_genres.intersection(item_genres)

        item_score += len(shared_genres) * 2

        scores[item['title']] = item_score    

    return scores

def get_recommendations(scores, limit = 3):
    positive_scores = {title:score for title,score in scores.items() if score > 0}

    sorted_scores = sorted(positive_scores.items(), key=lambda pair: pair[1], reverse = True)

    return sorted_scores[:limit]

def main():

    title_input = input("Enter a title you liked: ")

    selected_title = find_title(medialib, title_input)

    if selected_title is None:
        print("Title not found")
    else:
        scores = calculate_score(selected_title, medialib)

    recommendations = get_recommendations(scores)

    for title, score in recommendations:
        print(f"{title} -- Similarity Score: {score}")

    # print(f"Available moods: {moods}")
    # print("Type 'exit' or 'quit' at any time to quit the program")

    # while True:
    #     mood_input = input("What mood are you in? ").strip().lower()
    #     if mood_input in ['exit','quit']:
    #         break
    #     if mood_input not in moods:
    #         print("Choose one of the available moods ")
    #         continue
    #     type_input = input("Choose: 'movie' or 'show'? ").strip().lower()
    #     if type_input in ['exit','quit']:
    #         break
    #     if type_input not in ['movie', 'show']:
    #         print("Enter exactly 'movie' or 'show' ")
    #         continue
    #     genre_input = input("Enter a preferred genre, or press Enter to skip ").strip().lower()
    #     if genre_input in ['exit', 'quit']:
    #         break

    #     matches = find_recommendations(medialib, mood_input, type_input, genre_input)

    #     if matches:
    #         print("\nRecommendations:\n")

    #         for item in matches:
    #             print(f"Title: {item['title']}")
    #             print(f"Genres: {item['genres']}")
    #             print(f"Runtime: {item['runtime']}")
    #             print("-" * 40)
    #     else:
    #         print("Unfortunately a match was not found :(")

if __name__ == "__main__":
    main()