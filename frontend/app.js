const searchButton = document.getElementById("search-button")
const searchMovie = document.getElementById("movie-search")
const searchResults = document.getElementById("search-results")

searchButton.addEventListener("click", async () => {
    const query = searchMovie.value;

    const response = await fetch(`movies/search?query=${encodeURIComponent(query)}`);

    const movies = await response.json();

    // console.log(movies);

    searchResults.innerHTML = "";

    movies.forEach(movie => {
        const button = document.createElement("button");
        
        button.className = "search-result";

        button.textContent = `${movie.title} (${movie.release_date.slice(0,4)})`;

        searchResults.appendChild(button);

        button.addEventListener("click", () => {
            searchResults.innerHTML = "";
            getRecommendations(movie.id, movie.title);
        });
    });
});

async function getRecommendations(movieId, movieTitle) {
    const response = await fetch(`recommendations/${movieId}`);
    
    const recommendations = await response.json();

    const recommendationContainer = document.getElementById("recommendations");

    recommendationContainer.innerHTML = "";

    const heading = document.createElement("h2");

    heading.textContent = `Because you liked ${movieTitle}`;
    recommendationContainer.appendChild(heading);

    recommendations.forEach(movie => {
        const card = document.createElement("div");
        card.className = "recommendation-card";

        const title = document.createElement("h3");
        title.textContent = movie.title;

        const score = document.createElement("p");
        score.textContent = `Similarity score: ${movie.score}`;

        const reasons = document.createElement("p");
        reasons.textContent = movie.reasons.join(" * ");

        card.appendChild(title);
        card.appendChild(score);
        card.appendChild(reasons);

        recommendationContainer.appendChild(card);
    })
};
