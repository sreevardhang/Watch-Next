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

        if selectedtitle['mood'] == item['mood']:
            item_score += 3

        if selectedtitle['type'] == item['type']:
            item_score += 1

        item_genres = set(genre.strip().lower() for genre in item['genres'].split(','))

        shared_genres = selected_genres.intersection(item_genres)

        item_score += len(shared_genres) * 2

        scores[item['title']] = item_score    

    return scores

def get_recommendations(scores, limit=3):
    positive_scores = {title:score for title,score in scores.items() if score > 0}

    sorted_scores = sorted(positive_scores.items(), key=lambda pair: pair[1], reverse = True)

    return sorted_scores[:limit]

def main():

    title_input = input("Enter a title you liked: ")

    selected_title = find_title(medialib, title_input)

    if selected_title is None:
        print("Title not found")
        return
    
    scores = calculate_score(selected_title, medialib)
    recommendations = get_recommendations(scores)

    for title, score in recommendations:
        print(f"{title} -- Similarity Score: {score}")

if __name__ == "__main__":
    main()