import json

from pathlib import Path

clean_data_path = "C:/Users/tapis/PycharmProjects/Spotify_project/API_DATA_CLEAN"
final_list = []

pathlist = Path("C:/Users/tapis/PycharmProjects/Spotify_project/API_DATA").rglob('*.json')
for path in pathlist:
    filename = path.name.removesuffix('.json')
    # because path is object not string
    path_in_str = str(path)
    # print(path_in_str)
    # Opening JSON file
    f = open(path_in_str, 'r')
    print(path_in_str)

    data = json.load(f)
    songs_dict_list = []
    song_data_dict = {}
    keys = ["song_preview", "artists", "duration_ms", "song_name", "popularity"]
    values = []
    for i in range(0, len(data)):
        values.append(data[i]["track"]["preview_url"])
        values.append(data[i]["track"]["artists"][0]["name"])
        values.append(data[i]["track"]["duration_ms"])
        values.append(data[i]["track"]["name"])
        values.append(data[i]["track"]["popularity"])
        # print(values)
        # print(keys)
        songs_dict_list.append(dict(zip(keys, values)))
        values.clear()
    # print(songs_dict_list)
    final_list.extend(songs_dict_list)

with open(f"{clean_data_path}/final.json", "w") as outfile:
    json.dump(final_list, outfile)
print(final_list)
