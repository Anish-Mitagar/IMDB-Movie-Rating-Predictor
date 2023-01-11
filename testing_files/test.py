import movie_scraper
key = "k_frwsnx5q"
movie_name = 'The Amazing Spider-Man 2'
fake_movie_name = 'gergreerbe'
w0 = open("dataset.txt", "a")

movie_id = movie_scraper.get_movie_id(key, movie_name)
movie_id2 = movie_scraper.get_movie_id(key, fake_movie_name)

# print(movie_id)
# print(movie_id2)

movie_rating = movie_scraper.get_ratings(key, movie_id, movie_name)
#movie_rating2 = movie_scraper.get_ratings(key, movie_id2, fake_movie_name)

#print(movie_rating)
#print(movie_rating2[0])

movie_actors, movie_actors_ids  = movie_scraper.get_actors(key, movie_id, movie_name)
# movie_actors2, movie_actors_ids2 = movie_scraper.get_actors(key, movie_id2, fake_movie_name)

# print(movie_actors)
# print(movie_actors_ids)
# print(movie_actors2)
# print(movie_actors_ids2)

movie_num_wins, movie_num_nominations = movie_scraper.get_movie_awards(key, movie_id, movie_name)
#movie_awards2 = movie_scraper.get_movie_awards(key, movie_id2, fake_movie_name) 

#print(movie_awards)
#print(movie_awards2)

movie_actor_awards, cum_oscars, cum_wins, cum_nominations = movie_scraper.get_actors_awards(key, movie_actors_ids, movie_actors)

# print(movie_actor_awards)
# print(cum_oscars)
# print(cum_wins)
# print(cum_nominations)

# movie_actor_awards2, cum_oscars2, cum_wins2, cum_nominations2 = movie_scraper.get_actors_awards(key, movie_actors_ids2, movie_actors2)

# print(movie_actor_awards2)
# print(cum_oscars2)
# print(cum_wins2)
# print(cum_nominations2)

percent_male, percent_female, percent_under_30, percent_30_to_45, percent_over_45 = movie_scraper.get_gender_and_age_demographics(key, movie_id, movie_name)

data = (movie_name, movie_id, movie_rating[0], 
        movie_actors, movie_actors_ids, movie_num_wins, 
        movie_num_nominations, movie_actor_awards, 
        cum_oscars, cum_wins, cum_nominations, 
        percent_male, percent_female, percent_under_30, percent_30_to_45, percent_over_45)
    
if not all(data):
    print("FAILED: " + str(movie_name))


else:
    print("SUCESS: " + str(movie_name))

    data = {"movie name": movie_name, 
            "movie id": movie_id, 
            "movie rating": movie_rating[0], #y
            "movie num awards": movie_num_wins,
            "movie num nominations": movie_num_nominations,
            "percent male reviewers": percent_male, #x (0.0-1.0)
            "percent female reviewers": percent_female, #x (0.0-1.0)
            "percent under 30 reviewers": percent_under_30, #x (0.0-1.0)
            "percent 30-45 reviewers": percent_30_to_45, #x (0.0-1.0)
            "percent over 45 reviewers": percent_over_45, #x (0.0-1.0)
            "movie actor awards": movie_actor_awards,
            "cumulative actor oscars": cum_oscars, #x (a reasonable integer with no extreme values)
            "cumulative actor wins": cum_wins, #x (a reasonable integer with no extreme values)
            "cumulative actor nominations": cum_nominations} #x (a reasonable integer with no extreme values)
    
    w0.write((str(data)))
    w0.write('\n')
