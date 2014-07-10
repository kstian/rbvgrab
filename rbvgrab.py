import sys, getopt, urllib2, os, urllib, cookielib, ConfigParser, platform
from os import system

# helper function untuk parsing nilai konfigurasi ini style
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# fungsi untuk melakukan login
def login(mk, username, password):
    PHPSESSID = ''
    url = "http://www.pustaka.ut.ac.id/reader/index.php?modul="+str(mk) 
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(url)
    for cookie in cj:
        if cookie.name == 'PHPSESSID':
            PHPSESSID = cookie.value
    opener.addheaders.append(('Cookie', 'PHPSESSID='+PHPSESSID))
    print "Login menggunakan username : " + username
    data = urllib.urlencode({"username":username,"password":password, "_submit_check":"1", "submit":"submit"})
    request_object = urllib2.Request(url, data)
    response = opener.open(request_object)
    return PHPSESSID

def main(argv):
    t = ''
    c = ''
    d = ''
    modul=1
    isEndModul=False
    isEndPage=False
    mIndex=1
    pIndex=1
    totalPage=0
    global Config
    Config = ConfigParser.ConfigParser()
    Config.read("rbvgrab.ini")
    username = ConfigSectionMap("userinfo")["username"]
    password = ConfigSectionMap("userinfo")["password"]
    try:
        opts, args = getopt.getopt(argv,"hc:d:m:p:t:",["help", "cookie=","directory=","start-modul=","start-page="])
    except getopt.GetoptError:
        print 'rbvgrab.py -c <cookie_PHPSESSID_value> -d <directory>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'rbvgrab.py -c <cookie_PHPSESSID_value> -d <directory>'
            sys.exit()
        elif opt in ("-c", "--cookie"):
            c = arg
        elif opt in ("-d", "--directory"):
            d = arg
        elif opt in ("-m", "--start-modul"):
            mIndex = int(arg)
        elif opt in ("-p", "--start-page"):
            pIndex = int(arg)
        elif opt in ("-t", "--title"):
            t = arg
    c = login(d, username, password)
    print 'PHPSESSID = '+ str(c)
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'PHPSESSID='+c))
    opener.addheaders.append(('Referer', 'http://www.pustaka.ut.ac.id/reader/FlexPaperViewer.swf'))
    
    if not os.path.isdir(d):
        os.makedirs(d)
        FILE = open(d + "/0 " + t + ".txt", "wb")
        FILE.close()
    
    while isEndPage == False:
        content = opener.open("http://www.pustaka.ut.ac.id/reader/services/view.php?doc=M"+str(mIndex)+"&page="+str(pIndex))
        if content.info().getheader('Content-Type') == 'application/x-shockwave-flash':
            data = content.read()
            content.close()
            opener.close()
            FILE = open(d+"/M"+str(mIndex)+"P"+str(pIndex)+".swf", "wb")
            FILE.write(data)
            FILE.close()
            if platform.system() == 'Windows':
                system('TITLE Modul : '+str(mIndex) + ' Halaman : '+str(pIndex)+' disimpan...')
                system('CLS')
            print 'Memproses BMP : '+str(d) + ' ' + t
            print 'Modul : '+str(mIndex) + ' Halaman : '+str(pIndex)+' disimpan...'
            pIndex += 1
        elif pIndex == 1:
            isEndPage = True
        else:
            totalPage += pIndex
            pIndex = 1
            mIndex += 1
                
    print 'Proses selesai : '+str(totalPage)+' halaman berhasil disimpan.'
if __name__ == "__main__":
   main(sys.argv[1:])


