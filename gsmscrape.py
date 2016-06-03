import requests
import json
import time
import datetime
import re
gsm_makers = requests.get("http://www.gsmarena.com/makers.php3");
content = gsm_makers.text
split_content = content.split('<div class="st-text">');
split_content_main = split_content[1].split('</div>');
links = re.findall('<a href="?([^\s^"]+)>',split_content_main[0]);
count = 0
phone_count = 0
fo = open('gsmdata.json','a')
for u in links:
    if count%2==0:
        source_link = u
        try:
            get_maker_data = requests.get("http://www.gsmarena.com/"+source_link)
            read_maker_data = get_maker_data.text
            if '<div class="nav-pages">' in read_maker_data:
                get_pagination_content = read_maker_data.split('<div class="nav-pages">')
                get_pagination_content = get_pagination_content[1].split('</div>')
                get_pagination_links = re.findall(' href="?([^\s^"]+)',get_pagination_content[0])
                get_pagination_links.append(source_link)
            else:
                get_pagination_links.append(source_link)
            for p in get_pagination_links:
                try:
                    get_paginated_element = requests.get("http://gsmarena.com/"+p)
                    get_paginated_content = get_paginated_element.text
                    get_paginated_content = get_paginated_content.split('<div class="makers">')
                    get_paginated_content = get_paginated_content[1].split('</div>')
                    get_individual_phone_links = re.findall('<a href="?([^\s^]+)">',get_paginated_content[0])
                    for i in get_individual_phone_links:
                        try:
                            get_selected_page = requests.get('http://www.gsmarena.com/'+i)
                            get_selected_page_content = get_selected_page.text
                            model_image_link = re.findall('<img alt=[^>]+src=(.*?)>',get_selected_page_content)
                            if not model_image_link :
                                model_image_link = "NA"
                            else:
                                model_image_link = model_image_link[0].encode('utf-8')
                            # model_image_link = model_image_link[1]
                            # print(model_image_link)
                            model_full_name = re.findall('<title>(.*?)</title>',get_selected_page_content)
                            model_full_name = model_full_name[0].split(' - ')
                            model_full_name = model_full_name[0]
                            model_camera_specs = re.findall('<strong class="accent accent-camera">(.*?)<span>',get_selected_page_content)
                            if len(model_camera_specs)==0 or model_camera_specs[0]=="&nbsp;":
                                model_camera_specs = "NA"
                            else:
                                model_camera_specs = model_camera_specs[0].encode('utf-8')
                            # print(model_camera_specs)
                            model_ram_specs = re.findall('<strong class="accent accent-expansion">(.*?)<span>',get_selected_page_content)
                            if len(model_ram_specs)==0 or model_ram_specs[0]=="&nbsp;":
                                model_ram_specs = "NA"
                            else:
                                model_ram_specs = model_ram_specs[0].encode('utf-8')
                            # print(model_ram_specs)
                            model_battery_specs = re.findall('<strong class="accent accent-battery">(.*?)<span>',get_selected_page_content)
                            if len(model_battery_specs)==0 or model_battery_specs[0]=="&nbsp;" :
                                model_battery_specs = "NA"
                            else:
                                model_battery_specs = model_battery_specs[0].encode('utf-8')
                            # print(model_battery_specs)
                            get_selected_page_content = get_selected_page_content.split('<ul class="specs-spotlight-features" style="overflow:hidden;">')
                            get_selected_page_content = get_selected_page_content[1].split('</ul>')
                            model_internal_storage = re.findall('<span class="specs-brief-accent"><i class="head-icon icon-sd-card-0"></i>(.*?)</span>',get_selected_page_content[0])
                            if "RAM" not in model_internal_storage[0]:
                                if ',' in model_internal_storage[0]:
                                    model_internal_storage = model_internal_storage[0].split(',')
                                    if "MB" not in model_internal_storage[0] and "GB" in model_internal_storage[0]:
                                        model_internal_storage = model_internal_storage[0].replace("GB storage","")
                                        if '/' in model_internal_storage:
                                            model_internal_storage = model_internal_storage.split('/')
                                            model_internal_storage = model_internal_storage[0]
                                    else:
                                        model_internal_storage='NA'
                                    if model_ram_specs!='NA' and model_camera_specs!='NA' and model_battery_specs!='NA' and model_internal_storage!='NA' and float(model_ram_specs)<16.0 and float(model_camera_specs)>1.0 and float(model_battery_specs)>1100.0 :
                                        phone_count = phone_count + 1
                                        data = {}
                                        data["model_primary_id"] = phone_count
                                        data["model_full_name"] = model_full_name
                                        data["model_internal_storage"] = model_internal_storage
                                        data["model_camera_specs"] = model_camera_specs
                                        data["model_ram_specs"] = model_ram_specs
                                        data["model_battery_specs"] = model_battery_specs
                                        data["model_image_link"] = model_image_link
                                        data["model_updated_time"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                                        jsonify = json.dumps(data)
                                        fo.write(jsonify)
                                        fo.write(',')
                                        fo.write("\n")
                        except Exception as e:
                            print(e)
                            logging.exception("The following URL couldn't be reached:"+"http://www.gsmarena.com/"+i)
                except Exception as e:
                    print(e)
                    logging.exception("The following URL couldn't be reached: "+"http://www.gsmarena.com/"+p)
            count = count+1
        except Exception as e:
            print(e)
            logging.exception("The following URL couldn't be reached: "+"http://www.gsmarena.com/"+u)
    else:
        count = count+1
print(phone_count)
