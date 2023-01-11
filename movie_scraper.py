import requests
import json
import time
#3063
f = open("data_files/movienames.txt", "r")
names = f.readlines()

key = "k_frwsnx5q"

w0 = open("data_files/dataset.txt", "a")
w1 = open("data_files/scrapelog.txt", "a")

start = 0#int(input("Start Index: "))
end = start+2000 #len(names)
counter = 0
limit = 2000

#1 API Calls
def get_movie_id(key, movie_name):
    movie_id = None
    try:
        url = f"https://imdb-api.com/en/API/SearchTitle/{key}/{movie_name.lower().strip()}"
        movie_id = requests.get(url).json()["results"][0]["id"]

    except Exception as e:
        #print("Following error with " + str(movie_name))
        movie_id = None

    finally:
        return movie_id

#1 API Calls
def get_ratings(key, movie_id, movie_name):
    ratings = None
    try:
        r = f"https://imdb-api.com/en/API/Ratings/{key}/{movie_id}"
        response = requests.get(r).json()

        if type(response['imDb']) is float or int:
            imdb = response['imDb']
        else:
            imdb = -1
        if type(response['metacritic']) is float or int:
            meta = response['metacritic']
        else:
            meta = -1
        if type(response['theMovieDb']) is float or int:
            mvdb = response['theMovieDb']
        else:
            mvdb = -1
        if type(response['rottenTomatoes']) is float or int:
            rtom = response['rottenTomatoes']
        else:
            rtom = -1
        if type(response['filmAffinity']) is float or int:
            faff = response['filmAffinity']
        else:
            faff = -1
        ratings = [imdb, meta, mvdb, rtom, faff]

    except Exception as e:
        #print("Following error with " + str(movie_name))
        ratings = [None, None, None, None, None]

    finally:
        return ratings

#1 API Calls
def get_actors(key, movie_id, movie_name):
    actors = None
    actors_ids = None
    try:
        actors = []
        actors_ids = []
        mID = f"https://imdb-api.com/en/API/FullCast/{key}/{movie_id}"
        resp = requests.get(mID).json()

        for i in range(10):
            act = resp["actors"][i]["name"]
            act_id = resp["actors"][i]["id"]
            actors.append(act)
            actors_ids.append(act_id)
            if i==len(resp["actors"])-1:
                break

    except Exception as e:
        #print("Following error with " + str(movie_name))
        actors = None
        actors_ids = None

    finally:
        return actors, actors_ids

#1 API Calls   
def get_movie_awards(key, movie_id, movie_name):
    num_wins = None
    num_nominations = None
    try:
        data = f"https://imdb-api.com/en/API/Awards/{key}/{movie_id}"
        awards_data = requests.get(data).json()
        description = awards_data["description"]
        res = [int(i) for i in description.split() if i.isdigit()]
        num_wins = res[0]
        num_nominations = res[1]

    except Exception as e:
        #print("Following error with " + str(movie_name))
        num_wins = None
        num_nominations = None

    finally:
        return num_wins, num_nominations

#10 API Calls
def get_actors_awards(key, actor_ids, actor_names):
    actors_awards = []
    cum_oscars = 0
    cum_wins = 0
    cum_nominations = 0
    try:
        merged_list = tuple(zip(actor_ids, actor_names)) 
        for id, n in merged_list:
            num_oscars, num_wins, num_nominations = get_actor_awards(key, id, n)
            if num_oscars == None or num_wins == None or num_nominations == None:
                return None, None, None, None
            cum_oscars += num_oscars
            cum_wins += num_wins
            cum_nominations += num_nominations
            actors_awards.append((num_oscars, num_wins, num_nominations))
    except Exception as e:
        #print("get_actor_awards FAILED")
        actors_awards = None
        cum_oscars = None
        cum_wins = None
        cum_nominations = None
    finally:
        return actors_awards, cum_oscars, cum_wins, cum_nominations

#1 API Calls
def get_actor_awards(key, actor_id, actor_name):
    num_oscars = 0
    num_wins = 0
    num_nominations = 0
    try:
        data = f"https://imdb-api.com/en/API/Name/{key}/{actor_id}"
        awards_data = requests.get(data).json()
        description = awards_data["awards"]
        res = [int(i) for i in description.split() if i.isdigit()]
        if len(res) == 2:
            num_oscars = 0
            num_wins = res[0]
            num_nominations = res[1]
        if len(res) == 3:
            num_oscars = res[0]
            num_wins = res[1]
            num_nominations = res[2]

    except Exception as e:
        #print("Following error with " + str(actor_name))
        num_oscars = None
        num_wins = None
        num_nominations = None

    finally:
        return num_oscars, num_wins, num_nominations

#1 API Calls
def get_gender_and_age_demographics(key, movie_id, movie_name):
    percent_male = None
    percent_female = None
    percent_under_30 = None
    percent_30_to_45 = None
    percent_over_45 = None
    try:
        data = f"https://imdb-api.com/en/API/UserRatings/{key}/{movie_id}"
        demograph_data = requests.get(data).json()

        num_male = int(demograph_data["demographicMales"]["allAges"]["votes"])
        num_female = int(demograph_data["demographicFemales"]["allAges"]["votes"])
        percent_male = round((num_male / (num_male + num_female)),2)
        percent_female = round((num_female / (num_male + num_female)),2)

        num_under_30 = int(demograph_data["demographicAll"]["agesUnder18"]["votes"]) + int(demograph_data["demographicAll"]["ages18To29"]["votes"])
        num_30_to_45 = int(demograph_data["demographicAll"]["ages30To44"]["votes"])
        num_over_45 = int(demograph_data["demographicAll"]["agesOver45"]["votes"])
        num_all = num_under_30 + num_30_to_45 + num_over_45
        percent_under_30 = round(num_under_30/num_all, 2)
        percent_30_to_45 = round(num_30_to_45/num_all, 2)
        percent_over_45 = round(num_over_45/num_all, 2)

    except Exception as e:
        #print("Following error with " + str(movie_name))
        percent_male = None
        percent_female = None
        percent_under_30 = None
        percent_30_to_45 = None
        percent_over_45 = None

    finally:
        return percent_male, percent_female, percent_under_30, percent_30_to_45, percent_over_45
    
# for i in range (start, end):
#     #15 API Calls per film
#     if (counter == limit):
#         break
#     time.sleep(0.5)
#     movie_name = names[i]
#     movie_id = get_movie_id(key, movie_name)
#     movie_rating = get_ratings(key, movie_id, movie_name)
#     movie_actors, movie_actors_ids = get_actors(key, movie_id, movie_name)
#     movie_num_wins, movie_num_nominations = get_movie_awards(key, movie_id, movie_name)
#     movie_actors_awards, cum_actors_oscars, cum_actors_wins, cum_actors_nominations = get_actors_awards(key, movie_actors_ids, movie_actors)
#     movie_demographics0, movie_demographics1, movie_demographics2, movie_demographics3, movie_demographics4 = get_gender_and_age_demographics(key, movie_id, movie_name)

#     data = (movie_name, movie_id, movie_rating[0], 
#             movie_actors, movie_actors_ids, movie_num_wins, 
#             movie_num_nominations, movie_actors_awards, 
#             cum_actors_oscars, cum_actors_wins, cum_actors_nominations, 
#             movie_demographics0, movie_demographics1, movie_demographics2, movie_demographics3, movie_demographics4)
    
#     if not all(data):
#         print("FAILED: " + str(movie_name))
#         w1.write(("FAILED: " + str(movie_name)))
#         w1.write('\n')

#     else:
#         print("SUCESS: " + str(movie_name))
#         w1.write(("SUCESS: " + str(movie_name)))
#         w1.write('\n')
#         data = {"movie name": movie_name, 
#                 "movie id": movie_id, 
#                 "movie rating": movie_rating[0], #y
#                 "movie num awards": movie_num_wins,
#                 "movie num nominations": movie_num_nominations,
#                 "percent male reviewers": movie_demographics0, #x (0.0-1.0)
#                 "percent female reviewers": movie_demographics1, #x (0.0-1.0)
#                 "percent under 30 reviewers": movie_demographics2, #x (0.0-1.0)
#                 "percent 30-45 reviewers": movie_demographics3, #x (0.0-1.0)
#                 "percent over 45 reviewers": movie_demographics4, #x (0.0-1.0)
#                 "movie actor awards": movie_actors_awards,
#                 "cumulative actor oscars": cum_actors_oscars, #x (a reasonable integer with no extreme values)
#                 "cumulative actor wins": cum_actors_wins, #x (a reasonable integer with no extreme values)
#                 "cumulative actor nominations": cum_actors_nominations} #x (a reasonable integer with no extreme values)

#         w0.write((str(data)))
#         w0.write('\n')
#         counter += 1

# w0.close()
# w1.close()

# print("Scraped " + str(counter)+ "/2000 movies!")

# def to_Feature_Vector(actors, precentMaleAudience, percent30under, percent30_45, percent45over):
#     for actor in actors:


# def i():
#     data = f"https://imdb-api.com/en/API/SearchName/{key}/Natalie Portman"
#     data = requests.get(data).json()
#     data = data["results"][0]["id"]
#     return data

# a = i()
# print(a)

def to_Feature_Vector(actors, percentMale, percentu30, percent3045, percent45o):
    actor_ids = []
    for actor in actors:
        try:
            data = f"https://imdb-api.com/en/API/SearchName/{key}/{actor}"
            data = requests.get(data).json()
            data = data["results"][0]["id"]
            actor_ids.append(data)
        except Exception as e:
            continue


    _, cum_oscars, cum_wins, cum_nominations = get_actors_awards(key, actor_ids, actors)

    if cum_oscars is not None:
        norm_cum_oscars = (cum_oscars - 6.0135)/4.528639093
    else:
        norm_cum_oscars = 0
    if cum_wins is not None:
        norm_cum_wins = (cum_wins - 108.805)/77.9626068
    else:
        norm_cum_wins = 0
    if cum_nominations is not None:
        norm_cum_nominations = (cum_nominations - 208.6475)/153.6697838
    else:
        norm_cum_nominations = 0
    norm_percentMale = (percentMale - 0.796725)/0.106344624
    norm_percentu30 = (percentu30 - 0.13795)/0.076564539
    norm_percent3045 = (percent3045 - 0.610365)/0.077982417
    norm_percent45o = (percent45o - 0.251785)/0.113960332

    return [norm_percentMale, norm_percentu30, norm_percent3045, norm_percent45o, norm_cum_oscars, norm_cum_wins, norm_cum_nominations]

#print(test(["Natalie Portman"], 0.8, 0.33, 0.34, 0.33))