import requests
import json
from mega import Mega
import zipfile
import os

def get_mangadex_images_and_title(chapter_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Extract chapter ID from URL
    chapter_id = chapter_url.split("/")[-1]



    # Fetch image URLs
    api_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        base_url = data["baseUrl"]
        image_filenames = data["chapter"]["data"]
        image_urls = [f"{base_url}/data/{data['chapter']['hash']}/{img}" for img in image_filenames]
    else:
        print("Failed to fetch images. Status code:", response.status_code)
        image_urls = []

    return {
        "url": chapter_url,
        "img-urls": image_urls
    }


main_data = []

# Unzip temp.zip and extract temp.json
zip_file = "temp.zip"
extract_folder = "temp_extracted"

# Extract ZIP
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Load temp.json
json_file = os.path.join(extract_folder, "temp.json")

with open(json_file, 'r', encoding='utf-8') as f:
    main_data = json.load(f)


start_num = 0
end = start_num + 100000

main_data = main_data[start_num:end]


final_data = []
try:
    for index,obj in enumerate(main_data):
        if index <0:
            continue
        chapter_url = obj['href']
        if 'chapter' in chapter_url:
            try:
                
                chapter_data = get_mangadex_images_and_title(chapter_url)
                chapter_data['title'] = str(obj['text']).split("\n")[0]
                final_data.append(chapter_data)
            except Exception as e:
                print("Error 66")
        
finally:
        

    with open(f"{end}_img.json", 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
    mega = Mega()
    m= mega.login("afg154006@gmail.com",'megaMac02335!')
    try:
        m.upload("img.json")
    except Exception as e:
        print("error : 63",e)
    print("Data saved successfully to img.json!")
