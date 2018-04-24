#!/usr/bin/env python3.6
import mwclient, configparser, mwparserfromhell, argparse, re, pathlib,copy
from time import sleep
import timeit
import example

def figure_type(template):
    temp_template = copy.deepcopy(template)
   # temp_template.name = temp_template.name.lower()
    #temp_template = template
    temp_template.name = temp_template.name.lower()
    #template.name = template.name.lower()
    if temp_template.name.matches("infobox album"):
        return "infobox album"
    elif temp_template.name.matches("album infobox"):
        return "album infobox"
    elif temp_template.name.matches("album infobox soundtrack"):
        return "album infobox soundtrack"
    elif temp_template.name.matches("dvd infobox"):
        return "dvd infobox"
    elif temp_template.name.matches("infobox dvd"):
        return "infobox dvd"
    elif temp_template.name.matches("infobox ep"):
        return "infobox ep"
    elif temp_template.name.matches("extra chronology"):
        return "extra chronology"
    elif temp_template.name.matches("extra album cover"):
        return "extra album cover"
    elif temp_template.name.matches("extra track listing"):
        return "extra track listing"
    elif temp_template.name.matches("extra tracklisting"):
        return "extra tracklisting"
    else:
        return False
def figure_type2(template):
    #temp_template = copy.deepcopy(template)
    return example.template_figure_type(str(template.name))

def process_page():
    content_changed = False
    #text = " Jimmy had a jimmy bare. {{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}gg"
    code = mwparserfromhell.parse("Jimmy had a jimmy bare. {{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}{{info}}{{ce}}")
    for template in code.filter_templates():
        type_of_template = figure_type(template)
        if type_of_template:
            print(type_of_template)
def process_page2():
    content_changed = False
    #text = " Jimmy had a jimmy bare. {{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}g{{info}}{{ce}}{{cn}}{{album}}gg"
    code = mwparserfromhell.parse("Jimmy had a jimmy bare. {{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}h{{info}}{{ce}}{{cn}}{{album}}{{info}}{{ce}}")
    for template in code.filter_templates():
        type_of_template = figure_type2(template)
        if type_of_template != "":
            print(type_of_template)


if __name__ == "__main__":
    t = timeit.timeit('process_page()',setup='from timingtest2 import process_page', number=10000)
    print(str(t))
    t = timeit.timeit('process_page2()',setup='from timingtest2 import process_page2', number=10000)
    print(str(t))
    #process_page()
