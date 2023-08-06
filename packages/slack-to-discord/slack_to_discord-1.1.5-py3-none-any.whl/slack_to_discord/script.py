#!/usr/bin/env python

import json

discord = json.load(open("joypixels.raw.json"))
slack = json.load(open("iamcal.raw.json"))

def invert(m):
    r = {}
    for k, v in m.items():
        if isinstance(v, str):
            v = [v]
        for x in v:
            r[x] = k
    return r


conversions = {}

for k in set(discord) & set(slack):
    d = discord[k]
    s = slack[k]
    if isinstance(s, str):
        s = [s]
    if isinstance(d, str):
        d = [d]

    if any(x.startswith("flag_") for x in d):
        d = [x for x in d if x.startswith("flag_")]

    for x in s:
        if x.startswith("skin-tone-"):
            continue
        x = x[0] + x[1:].replace("-", "_")
        if x not in d:
            conversions[x] = d[0]

breakpoint()
