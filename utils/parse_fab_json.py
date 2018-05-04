import os
import json


SOURCE_FILE_DIR = "source_files"
OUT_PUT_DIR = "fab_json"


def parse_fab_file(source_file, target_file):
    with open(source_file) as f:
        lines = f.readlines()

    content = []
    for file_name in lines:
        filtered = file_name.strip(" \n").split("#")[0].replace("\\", "/")
        if filtered:
            content.append(filtered)

    fab_json = {
        "type": "filelist",
        "signal_mods": [],
        "statics_cdn": [],
        "spec_files": [],
        "apps": [],
        "djapps": [],
        "common": [],
        "fix_common": []
    }
    fab_json["signal_mods"] = content[0].split(" ")
    content = content[1:]

    # pick statics files
    for file_name in content:
        base, ex = os.path.splitext(file_name)
        if ex in (".js", "png") and file_name not in fab_json["statics_cdn"]:
            fab_json["statics_cdn"].append(file_name)

    # pick spec_files
    fab_json["spec_files"].extend(content)

    # pick apps and djapps
    for file_name in content:
        s = file_name.split("/")
        if s[0] == "apps":
            if s[1] not in fab_json["apps"]:
                fab_json["apps"].append(s[1])
        elif s[0] == "djapps":
            if s[1] not in fab_json["djapps"]:
                fab_json["djapps"].append(s[1])
        else:
            if s[0] not in fab_json["common"]:
                fab_json["common"].append(s[0])
            if file_name not in fab_json["fix_common"]:
                fab_json["fix_common"].append(file_name)

    with open(target_file, "w") as f:
        f.write(json.dumps(fab_json, indent=4, ensure_ascii=False))
    print "gen: %s" % target_file


if __name__ == "__main__":
    source_files = os.listdir(SOURCE_FILE_DIR)
    gen_file_list = {}
    for f in source_files:
        base_name, ex_name = os.path.splitext(f)
        gen_file_list[f] = base_name + ".json"

    existed_json_files = os.listdir(OUT_PUT_DIR)
    need_gen_files = {k: v for k, v in gen_file_list.iteritems()}  # if v not in existed_json_files}

    for src in need_gen_files:
        parse_fab_file(os.path.join(SOURCE_FILE_DIR, src), os.path.join(OUT_PUT_DIR, need_gen_files[src]))
    print "Done"
