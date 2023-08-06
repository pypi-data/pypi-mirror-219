"""doc"""
print("Hello")

worked_list = [
    {"Call": "K5TUX", "Band": 14.0},
    {"Call": "K5TUX", "Band": 21.0},
    {"Call": "N2CQR", "Band": 14.0},
    {"Call": "NE4RD", "Band": 14.0},
]

temp = {}

for worked_dict in worked_list:
    call = worked_dict.get("Call")
    if call in temp:
        bandlist = temp[call]
        bandlist.append(worked_dict["Band"])
        temp[call] = bandlist
        continue
    temp[call] = [worked_dict["Band"]]

print(f"{temp}")
