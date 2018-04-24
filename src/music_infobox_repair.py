#!/usr/bin/env python3.6
import mwclient, configparser, mwparserfromhell, argparse, re, pathlib,copy
import music_infobox
from time import sleep

def call_home(site):
    # page = site.Pages['User:' + config.get('enwiki','username') + "/status"]
    page = site.Pages['User:DeprecatedFixerBot/status']
    text = page.text()
    if "false" in text.lower():
        return False
    return True


def allow_bots(text, user):
    user = user.lower().strip()
    text = mwparserfromhell.parse(text)
    for tl in text.filter_templates():
        if tl.name in ('bots', 'nobots'):
            break
    else:
        return True
    for param in tl.params:
        bots = [x.lower().strip() for x in param.value.split(",")]
        if param.name == 'allow':
            if ''.join(bots) == 'none': return False
            for bot in bots:
                if bot in (user, 'all'):
                    return True
        elif param.name == 'deny':
            if ''.join(bots) == 'none': return True
            for bot in bots:
                if bot in (user, 'all'):
                    return False
    return True


def save_edit(page, utils, text):
    config = utils[0]

    site = utils[1]
    dry_run = utils[2]
    original_text = text
    if not dry_run:
        if not allow_bots(original_text, config.get('enwikidep', 'username')):
            print("Page editing blocked as template preventing edit is present.")
            return
    # print("{}".format(dry_run))
    code = mwparserfromhell.parse(text)
    for template in code.filter_templates():
        if template.name.matches("nobots") or template.name.matches("Wikipedia:Exclusion compliant"):
            if template.has("allow"):
                if "DeprecatedFixerBot" in template.get("allow").value:
                    break  # can edit
            print("\n\nPage editing blocked as template preventing edit is present.\n\n")
            return
    if not call_home(site):  # config):
        raise ValueError("Kill switch on-wiki is false. Terminating program.")
    time = 0
    edit_summary = """Removed deprecated parameter(s) from [[Template:Infobox album]]/[[Template:Extra chronology]]/[[Template:Extra album cover]]/[[Template:Extra track listing]] using [[User:""" + config.get(
        'enwikidep', 'username') + "| " + config.get('enwikidep',
                                                     'username') + """]]. Questions? [[User talk:TheSandDoctor|msg TSD!]] (please mention that this is task #3! [[Wikipedia:Bots/Requests for approval/DeprecatedFixerBot 3|BRFA in-progress]])"""
    while True:
        # text = page.edit()
        if time == 1:
            text = site.Pages[page.page_title].text()
        try:
            content_changed, text = process_page(original_text)
        except ValueError as e:
            """
            To get here, there must have been an issue figuring out the
            contents for the parameter colwidth.

            At this point, it is safest just to print to console,
            record the error page contents to a file in ./errors and append
            to a list of page titles that has had
            errors (error_list.txt)/create a wikified version of error_list.txt
            and return out of this method.
            """
            print(e)
            pathlib.Path('./errors').mkdir(parents=False, exist_ok=True)
            title = get_valid_filename(page.page_title)
            text_file = open("./errors/err " + title + ".txt", "w")
            text_file.write("Error present: " + str(e) + "\n\n\n\n\n" + text)
            text_file.close()
            text_file = open("./errors/error_list.txt", "a+")
            text_file.write(page.page_title + "\n")
            text_file.close()
            text_file = open("./errors/wikified_error_list.txt", "a+")
            text_file.write("#[[" + page.page_title + "]]" + "\n")
            text_file.close()
            return
        try:
            if dry_run:
                print("Dry run")
                # Write out the initial input
                title = get_valid_filename(page.page_title)
                text_file = open("./tests/in " + title + ".txt", "w")
                text_file.write(original_text)
                text_file.close()
                # Write out the output
                if content_changed:
                    title = get_valid_filename(page.page_title)
                    text_file = open("./tests/out " + title + ".txt", "w")
                    text_file.write(text)
                    text_file.close()
                else:
                    print("Content not changed, don't print output")
                break
            else:
                 #   print("Would have saved here")
                 #   break
                # TODO: Enable
                page.save(text, summary=edit_summary, bot=True, minor=True)
                print("Saved page")
                if example.leftMess(site,page.page_title):
                    print("Introduced error, self reverted")
        except mwclient.ProtectedPageError:
            print('Could not edit ' + page.page_title + ' due to protection')
        except mwclient.EditError:
            print("Error")
            time = 1
            sleep(5)  # sleep for 5 seconds before trying again
            continue
        break


def get_valid_filename(s):
    """
    Turns a regular string into a valid (sanatized) string that is safe for use
    as a file name.
    Method courtesy of cowlinator on StackOverflow
    (https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename)
    @param s String to convert to be file safe
    @return File safe string
    """
    assert (s is not "" or s is not None)
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


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


def process_page(text):
    content_changed = False

    code = mwparserfromhell.parse(text)
    for template in code.filter_templates():
        type_of_template = figure_type(template)
        if type_of_template:
            try:
                #t = copy.deepcopy(template)
                #parat = str(t.params).lower()
                #t = mwparserfromhell.nodes.template.Template(str(t),parat)
                #print(t.params)
                if type_of_template == "extra chronology":
                    wikilink1 = re.compile(r"(\[\[(?:(?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:\d\d+\s*)?(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+)|(\d\d+-\d\d-\d\d+)))")
                    datetempreg = re.compile(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))")
                    datetempreg2 = re.compile(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))")
                    datetempreg3 = re.compile(r"\d\d\d+")
                    if template.has("this album"):
                        #wikilink1 = re.compile(r"(\[\[(?:(?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:\d\d+\s*)?(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+)|(\d\d+-\d\d-\d\d+)))")

                        print("Has this album")
                        re1 = datetempreg.search(str(template.get('this album').value).strip(),re.IGNORECASE)
                        re2 = datetempreg2.search(str(template.get('this album').value).strip(),re.IGNORECASE)
                        #re1 = re.search(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))",str(template.get('this album').value).strip(),re.IGNORECASE)
                        #re2 = re.search(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))",str(template.get('this album').value).strip(),re.IGNORECASE)
                        #template.get("this album","title")
                        template.get("this album").name = "title"
                        if not re1:
                            if not re2:
                                print("Didn't happen extra chronology")
                                continue
                        t = wikilink1.search(str(template.get('title').value).strip(),re.IGNORECASE)
                        #t = re.search(r"(\[\[(?:(?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:\d\d+\s*)?(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+)|(\d\d+-\d\d-\d\d+)))",str(template.get('title').value).strip(),re.IGNORECASE)
                        #t1 = re.search(r"(\[\[(?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))",str(template.get('title').value).strip(),re.IGNORECASE)
                        if not t:
                            print("Not t")
                            template.get("title").value = re.sub(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:\d\d+\s*)?(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))","",str(template.get('title').value))
                    #    if not t1:
                    #        print("Not t1")
                    #        template.get("title").value = re.sub(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))","",str(template.get('title').value))
                            #FIXME: Never being called?
                        if re1:
                            template.add("year",re1.group(1))
                        if re2:
                            template.add("year",re2.group(1))
                    if template.has("last album"):
                        print("Has last album")
                        re1 = datetempreg.search(str(template.get('last album').value).strip(),re.IGNORECASE)
                        re2 = datetempreg2.search(str(template.get('last album').value).strip(),re.IGNORECASE)
                        re3 = datetempreg3.search(str(template.get('last album').value).strip(), re.IGNORECASE)
                        #re1 = re.search(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))",str(template.get('last album').value).strip(),re.IGNORECASE)
                        #re2 = re.search(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))",str(template.get('last album').value).strip(),re.IGNORECASE)
                        #template.replace("previous album","prev_title")
                        template.get("last album").name = "prev_title"
                        if not re1:
                            if not re2:
                                if not re3:
                                    print("Didn't happen last album")
                                    continue
                        t = re.search(r"(\[\[(?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))",str(template.get('prev_title').value).strip(),re.IGNORECASE)
                        t1 = re.search(r"(\[\[(?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+)|(\d\d\d+))",str(template.get('prev_title').value).strip(),re.IGNORECASE)
                        if not t:
                            template.get("prev_title").value = re.sub(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))","",str(template.get('prev_title').value))
                        if not t1:
                            template.get("prev_title").value = re.sub(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))|(\d\d\d+))","",str(template.get('prev_title').value))
                        if re1:
                            template.add("prev_year",re1.group(1))
                            t = re.search(r"(\[\[(?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))",str(template.get('prev_title').value).strip(),re.IGNORECASE)
                            t1 = re.search(r"(\[\[(?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))",str(template.get('prev_title').value).strip(),re.IGNORECASE)
                            if not t:
                                template.get("prev_title").value = re.sub(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))","",str(template.get('prev_title').value))
                            if not t1:
                                template.get("prev_title").value = re.sub(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))","",str(template.get('prev_title').value))

                        if re2:
                            template.add("prev_year",re2.group(1))

                    if template.has("next album"):
                        print("Has next album")
                        re1 = datetempreg.search(str(template.get('next album').value).strip(),re.IGNORECASE)
                        re2 = datetempreg2.search(str(template.get('next album').value).strip(),re.IGNORECASE)
                        #re1 = re.search(r"((?:\d\d?\/\d\d?\/\d\d\d+)|(?:\d\d?\d+\/\d\d?\/\d\d?)|(?:(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d?,?\s*\d\d\d+))",str(template.get('next album').value).strip(),re.IGNORECASE)
                        #re2 = re.search(r"((?:(?:\d\d+\s*)?(?:(?:Jan|January|Feb|February|March|Mar|Apr|April|May|June|July|August|Aug|Sept|September|Oct|October|Nov|November|Dec|December))\s*\d\d\d+)|(\d\d+-\d\d-\d\d+))",str(template.get('next album').value).strip(),re.IGNORECASE)
                        #template.replace("next album","next_title")
                        template.get("next album").name = "next_title"
                        if not re1:
                            if not re2:
                                print("Didn't happen next album")
                                continue
                        if re1:
                            template.add("next_year",re1.group(1))
                        if re2:
                            template.add("next_year",re2.group(1))

                if template.has("released"):
                    #print("Y")
                    print(str(template.get('released').value).strip())
                    if not re.search(r'\d\d\d+',str(template.get('released').value).strip()):
                        print("Didn't happen released")
                        continue
                # name = template.name
                # template.name = "d" + temp
                template.name = "subst:" + type_of_template + "|"
                # template.name = "subst:" + template.name
                content_changed = True  # do_cleanup_columns_list(template)
                print("params " + str(type_of_template))
            except ValueError:
                raise
    return [content_changed, str(code)]  # get back text to save


def single_run(title, utils, site,cat_to_avoid):
    if title is None or title is "":
        raise ValueError("Category name cannot be empty!")
    if utils is None:
        raise ValueError("Utils cannot be empty!")
    if site is None:
        raise ValueError("Site cannot be empty!")
    avoid = []
    if cat_to_avoid is not None:
        avoid = music_infobox.gen_cat_to_avoid(site,cat_to_avoid)
        #for page in site.Categories[cat_to_avoid]:
        #    avoid.append(page.name)
    print(title)
  #  print(avoid)
    if music_infobox.inlist(title,pages_to_avoid):
    #if title in avoid:
        print("Page should be avoided!")
        exit(0)
    page = site.Pages[title]  # '3 (Bo Bice album)']
    text = page.text()

    try:
        # utils = [config,site,dry_run]
        save_edit(page, utils, text)  # config, api, site, text, dry_run)#, config)
    except ValueError as err:
        print(err)


def category_run(cat_name, utils, site, offset, limited_run, pages_to_run, cat_to_avoid):
    if cat_name is None or cat_name is "":
        raise ValueError("Category name cannot be empty!")
    if utils is None:
        raise ValueError("Utils cannot be empty!")
    if site is None:
        raise ValueError("Site cannot be empty!")
    if offset is None:
        raise ValueError("Offset cannot be empty!")
    if limited_run is None:
        raise ValueError("limited_run cannot be empty!")
    if pages_to_run is None:
        raise ValueError("""Seriously? How are we supposed to run pages in a
        limited test if none are specified?""")
    counter = 0
    pages_to_avoid = []
    #for page in site.Categories[cat_to_avoid]:
    #    pages_to_avoid.append(page.name)
    pages_to_avoid = music_infobox.gen_cat_to_avoid(site,cat_to_avoid)
    for page in site.Categories[cat_name]:
        if music_infobox.inlist(page.name,pages_to_avoid):
        #if page.name in pages_to_avoid:
            print("Page in pages to avoid! CONTINUING!")
            continue
        # to get this far, page isn't in category to avoid
        if offset > 0:
            offset -= 1
            print("Skipped due to offset config")
            continue
        print("Working with: " + page.name + " " + str(counter))
        if limited_run:
            if counter <= pages_to_run:
                counter += 1
                text = page.text()
                try:
                    save_edit(page, utils, text)  # config, api, site, text, dry_run)#, config)
                except ValueError as err:
                    print(err)
            else:
                return  # run out of pages in limited run


def main():
    dry_run = False
    pages_to_run = 5
    offset = 0
    category = "Music infoboxes with deprecated parameters"  # "Pages using div col with deprecated parameters"
    category_to_avoid = "Music infoboxes with Module:String errors"
    limited_run = True

    parser = argparse.ArgumentParser(prog='DeprecatedFixerBot Music infobox fixer', description='''Adds "subst:" to the beginning of all
    {{infobox album}}, {{extra chronology}}, {{extra album cover}}, and {{extra track listing}} templates. This results in the template substitution trick which replaces deprecated parameters with their correct values to occur.''')
    parser.add_argument("-dr", "--dryrun", help="perform a dry run (don't actually edit)",
                        action="store_true")
    # parser.add_argument("-arch","--archive", help="actively archive Tweet links (even if still live links)",
    #                action="store_true")
    args = parser.parse_args()
    if args.dryrun:
        dry_run = True
        print("Dry run")

    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')
    if dry_run:
        pathlib.Path('./tests').mkdir(parents=False, exist_ok=True)
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    try:
        # pass
        site.login(config.get('enwikidep', 'username'), config.get('enwikidep', 'password'))
    except mwclient.LoginError as e:
        # print(e[1]['reason'])
        print(e)
        raise ValueError("Login failed.")
    utils = [config, site, dry_run]
    try:
        category_run(category,utils,site,offset,limited_run,pages_to_run,category_to_avoid)
    #    single_run("Brazil (EP)", utils, site, category_to_avoid)

        #single_run("De Viaje", utils, site, category_to_avoid)
    #    single_run("User:DeprecatedFixerBot/sandbox/music infoboxes", utils, site, category_to_avoid)
    except ValueError as e:
        print("\n\n" + str(e))


if __name__ == "__main__":
    main()

def query():
    result = site.api('query',format='json',list='recentchanges',rcuser='DeprecatedFixerBot',rcprop='title|timestamp|comment',rclimit='max',rctype='categorize')
    res2 = result['query']['recentchanges']

    t_f = open("pi.txt",'w+')
    check = re.compile(r'(\[\[.+\]\])')
    for i in res2:
        title = list(i.items())[2][1]
        comment = list(i.items())[4][1]
        if title == "Category:Music infoboxes with Module:String errors":
            print("YOYO")
            #t_f = open("pi.txt",'a')
            cmt = re.match(check,comment)
            t_f.write(str(title) + " " + str(cmt.group(1)) + "\n")

    #    tit.append(title)
        #print(title)
    t_f.close()
    print(list(res2[2].items()))
    text_file = open("result.txt", "w")
    text_file.write(str(result['query']))
    text_file.close()
