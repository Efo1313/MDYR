import requests
import re
import json

base_url = "https://cdn4.gledam.xyz/hls/hd-btv-hd"
url = "https://seirsanduk.online/?player=2&id=hd-btv-hd&pass="
response = requests.get(url)

if response.status_code == 200:
    site_content = response.text
    match = re.search(r'ht_stream_m3u8":"(.*?)"', site_content)
    
    if match:
        json_data = match.group(1)
        json_data_valid = json_data.replace("\\/", "/")  # Replace escaped slashes
        
        try:
            ht_data = json.loads('{"ht_stream_m3u8":"' + json_data_valid + '"}')
            ht_stream_mpg = ht_data.get('ht_stream_mpg')
            
            if ht_stream_m3u8:
                #print(f"Found Live URL: {ht_stream_mpg}")
                content_response = requests.get(ht_stream_m3u8)
                
                if content_response.status_code == 200:
                    content = content_response.text
                    lines = content.split("\n")
                    modified_content = ""
                    
                    for line in lines:
                        if line.startswith("bnt1"):
                            full_url = base_url + line
                            modified_content += full_url + "\n"
                        else:
                            modified_content += line + "\n"
                    
                    print(modified_content)
                else:
                    print("Error fetching content from the Live URL.")
            else:
                print("Live URL not found in the content.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
    else:
        print("Live URL pattern not found in the content.")
else:
    print("Error: Status code is not 200.")
