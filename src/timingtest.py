import timeit
import mwclient
import example

def main():
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')
    site.login('DeprecatedFixerBot', 'PvDF5hBf;;Ibq#lb)06BYnz}LB{|l!rj')
    #pages_to_avoid = []
    #print(timeit.timeit('addme(site)',setup="import mwclient site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')",number=10))
    #p = site.Pages['Rolling Stones']
    #print(timeit.timeit('addme(site)')
#    for page in site.Categories['Music infoboxes with Module:String errors']:
        #print(page)
#        pages_to_avoid.append(page.name)
#    print(pages_to_avoid)
pages_to_avoid = []
if __name__=='__main__':
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')
    site.login('DeprecatedFixerBot', 'PASSWORD')
#    pages_to_avoid = []
    #p = site.Pages['Rolling Stones']
    for page in site.Categories['Music infoboxes with Module:String errors']:
        #print(page)
        pages_to_avoid.append(page.name)
    #addme()
    #t = timeit.timeit(stmt='addme()', setup='from timingtest import addme',number=1)
    t = timeit.timeit(stmt='me()', setup='from timingtest import me',number=1)
    print("Vanilla " + str(t))
    t = timeit.timeit(stmt="inlist('Dark Christmas',pages_to_avoid)",setup="from example import inlist; from timingtest import pages_to_avoid")
    #t.timeit()
    print("C++ " + str(t))
    #print(timeit.timeit('addme()',setup='import mwclient', globals=globals()))
    #main()
def addme():
    site = mwclient.Site(('https', 'en.wikipedia.org'), '/w/')
    site.login('DeprecatedFixerBot', 'PvDF5hBf;;Ibq#lb)06BYnz}LB{|l!rj')
#    pages_to_avoid = []
    #p = site.Pages['Rolling Stones']
    for page in site.Categories['Music infoboxes with Module:String errors']:
        #print(page)
        pages_to_avoid.append(page.name)
def me():
    if "Dark Christmas" in pages_to_avoid:
        pass
    #    print("YO")
    else:
        pass
    #    print("Bo")
