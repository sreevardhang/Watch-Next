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

    selected_genres = set(genre.strip().lower() for genre in selectedtitle['genres'].split(','))

    for item in medialist:
        if selectedtitle['title'] == item['title']:
            continue

        item_score = 0
        reasons = []

        if selectedtitle['mood'] == item['mood']:
            item_score += 3
            reasons.append("matching mood")

        if selectedtitle['type'] == item['type']:
            item_score += 1
            reasons.append("matching type")

        item_genres = set(genre.strip().lower() for genre in item['genres'].split(','))

        shared_genres = selected_genres.intersection(item_genres)

        if shared_genres:
            item_score += len(shared_genres) * 2
            reasons.append(f"shared genres: {', '.join(sorted(shared_genres))}")

        scores[item["title"]] = {"score": item_score, "reasons": reasons}

    return scores

def get_recommendations(scores, limit=3):
    positive_scores = {title: details for title, details in scores.items() if details["score"] > 0}

    sorted_scores = sorted(positive_scores.items(), key=lambda pair: pair[1]["score"], reverse = True)

    return sorted_scores[:limit]

def main():

    print("Media Recommendation Engine")
    print("Type 'exit' or 'quit' to close the program")

    while(True):
        title_input = input("Enter a title you liked: ")
        if title_input.strip().lower() in ['exit', 'quit']:
            return
        selected_title = find_title(medialib, title_input)

        if selected_title is None:
            print("Title not found")
            continue
        
        scores = calculate_score(selected_title, medialib)
        recommendations = get_recommendations(scores)
        print("\n")
        print("Your recommendations (top 3): ")
        for title, details in recommendations:
            print(f"{title}")
            print(f"Similarity Score: {details['score']}")
            print(f"Reasons: {', '.join(details['reasons'])}")
            print("\n")

if __name__ == "__main__":
    main()