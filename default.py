import os, sys
import xbmc, xbmcgui, xbmcaddon
import time
import codecs, shutil
import ftplib
import urllib2
import json

ADDON     = xbmcaddon.Addon(id='script.html.library-report')
ADDON_NAME = ADDON.getAddonInfo('name')
LANGUAGE  = ADDON.getLocalizedString
ICON      = ADDON.getAddonInfo('icon')
CWD       = ADDON.getAddonInfo('path').decode("utf-8")
RESOURCE  = xbmc.translatePath(os.path.join(CWD, 'resources').encode("utf-8")).decode("utf-8")
DATA      = xbmc.translatePath(os.path.join(RESOURCE, 'data').encode("utf-8")).decode("utf-8")
IMAGE     = xbmc.translatePath(os.path.join(RESOURCE, 'images').encode("utf-8")).decode("utf-8")

# get addon settings
file_path = ADDON.getSetting('save_location')
enable_password = ADDON.getSetting('Enable_Password')
include_movies = ADDON.getSetting('includemovies')
plot_movies = ADDON.getSetting('movieplot')
include_tvshows = ADDON.getSetting('includetvshows')
plot_tvshows = ADDON.getSetting('tvshowplot')
enable_ftp = ADDON.getSetting('Enable_ftp')
host = ADDON.getSetting('server')
user = ADDON.getSetting('user')
password = ADDON.getSetting('password')
change_ftp_dir = ADDON.getSetting('enable_ftp_dir')
directory = ADDON.getSetting('ftp_dir')
web_root = ADDON.getSetting('web_root')
web_password = ADDON.getSetting('web_password')
logout = ADDON.getSetting('logout_url')

# file locations/names & paths
while file_path=="":
    xbmcgui.Dialog().ok(ADDON_NAME,LANGUAGE(30004))
    ADDON.openSettings()
    file_path = ADDON.getSetting('save_location')

file_name = 'index.html'
data_files = os.listdir(DATA)
image_files = os.listdir(IMAGE)
image_dest = os.path.join(file_path, 'images')
f_http = codecs.open(os.path.join(file_path,str(file_name)), "w", encoding="utf-8")
pDialog = xbmcgui.DialogProgressBG()

# data
pDialog.create(ADDON_NAME, '')
pDialog.update(0, message=LANGUAGE(30034))
if (include_movies == 'true') and xbmc.getCondVisibility("Library.HasContent(Movies)"):
    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties" : ["genre", "studio", "plotoutline", "plot", "rating", "year", "mpaa", "imdbnumber", "streamdetails", "top250", "runtime"], "sort": { "order": "ascending", "method": "title", "ignorearticle": true } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    movies = jsonobject["result"]["movies"]
    pDialog.update(25, message=LANGUAGE(30034))

if (include_tvshows == 'true') and xbmc.getCondVisibility("Library.HasContent(TVShows)"):
    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["genre", "title", "studio", "season", "episode", "plot", "rating", "year", "mpaa", "imdbnumber"], "sort": { "order": "ascending", "method": "title" } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    tvshows = jsonobject["result"]["tvshows"]
    pDialog.update(75, message=LANGUAGE(30034))

    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["tvshowid", "episode", "season", "streamdetails", "runtime"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    episodes = jsonobject["result"]["episodes"]
    pDialog.update(100, message=LANGUAGE(30034))

xbmc.sleep(200)
pDialog.close()

# create html output
def main():
    # password_protect
    if (enable_password == 'true'):
        f_http.write('\n')
    f_http.write('<!DOCTYPE html>\n')
    f_http.write('<head>\n')
    f_http.write('<meta  content="text/html;  charset=UTF-8"  http-equiv="Content-Type">\n')
    f_http.write('<link rel="shortcut icon" href="images/favicon.ico">\n')
    f_http.write('<link rel="icon" sizes="16x16 32x32 64x64" href="images/favicon.ico">\n')
    f_http.write('<title>Kodi '+LANGUAGE(30007)+'</title>\n')
    f_http.write('<link rel="stylesheet" href="Default.css">\n')
    f_http.write("</head>\n")
    f_http.write('<body background="images/bg.png">\n')
    f_http.write('<div id="header" style="height:95px;width:90%;position : fixed;background-color:#333333;margin-left: 5%;margin-right: auto ;">\n')
    f_http.write('<div id="Date" style="height:95px;width:20%;float:right;padding-right:1%;padding-top:15px;">\n')
    f_http.write('<p class="date">'+LANGUAGE(30012)+time.strftime('%d %B %Y')+'</p>\n')
    # password_protect logout
    if (enable_password == 'true'):
        f_http.write('<form style="float:right;padding-top:30px;" method="get" action="password_protect.php" /><input type="submit" value="Logout" /><input type="hidden" name="logout" value="1" /></form>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Links" style="height:95px;width:20%;float:left;padding-left:1%;">\n')
    if (include_movies == 'true') and (include_tvshows == 'true'):
        f_http.write('<p class="links"><a href="#movie_link">'+xbmc.getLocalizedString(342)+'</a>&nbsp;&nbsp;<a href="#tvshow_link">'+xbmc.getLocalizedString(20343)+'</a></p>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Heading" style="height:95px;width:80%;margin-left: auto;margin-right: auto ;">\n')
    f_http.write('<h1><a href="http://kodi.tv/" target="_blank"><img src="images/logo.png" alt="Kodi" width="150" height="52" align="center"></a> '+LANGUAGE(30007)+'</h1>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Body" style="width:100%;padding-top:75px;">\n')

    if (include_movies == 'true') and xbmc.getCondVisibility("Library.HasContent(Movies)"):
        f_http.write('<a class="anchor" id="movie_link">anchor</a>\n')
        f_http.write('<table class="gridtable">\n')
        f_http.write('<tr>\n')
        f_http.write('<th colspan="6"><span style="text-transform: uppercase">'+xbmc.getLocalizedString(342)+':</span> ('+str(len(movies))+')</th>\n')
        f_http.write('</tr>\n')
        pDialog.create(LANGUAGE(30033), '')
        moviecount = 0
        for movie in movies:
            moviegenre = " / ".join(movie['genre'])
            moviestudio = " / ".join(movie['studio'])
            movie_rating = str(round(float(movie['rating']),1))+' &#9733;'
            movie_runtime = '%s min' % str(movie['runtime'] / 60)
            if movie['streamdetails']['video'] != []:
                videowidth = movie['streamdetails']['video'][0]['width']
                videoheight = movie['streamdetails']['video'][0]['height']
                if videowidth >= 1280 or videoheight >= 720:
                    videoresolution = '<img src="images/hd.png" alt="HD" width="24" height="15">'
                else:
                    videoresolution = '<img src="images/sd.png" alt="SD" width="24" height="15">'
            f_http.write('<tr class="table">\n')
            f_http.write('<td width="30%">\n')
            f_http.write('<div style="float:left;width:95%;"><b><a href="http://www.imdb.com/title/'+str(movie['imdbnumber'])+'/" target="_blank">'+movie['label']+'</a></b> ('+str(movie['year'])+')</div>\n')
            f_http.write('<div style="float:right;width:5%;">'+str(videoresolution)+'</div>\n')
            f_http.write('</td>\n')
            f_http.write('<td width="4%" align="center">'+str(movie_rating)+'</td>\n')
            f_http.write('<td width="5%" align="center">'+str(movie_runtime)+'</td>\n')
            f_http.write('<td width="25%">'+str(moviegenre)+'</td>\n')
            f_http.write('<td width="15%">'+moviestudio+'</td>\n')
            # format movie mpaa
            if str(movie['mpaa']).startswith(LANGUAGE(30014)):
                f_http.write('<td>'+str(movie['mpaa'])+'</td>\n')
            elif str(movie['mpaa']) == "":
                f_http.write('<td>'+LANGUAGE(30014)+' NA</td>\n')
            else:
                f_http.write('<td>'+LANGUAGE(30014)+' '+str(movie['mpaa'])+'</td>\n')
            f_http.write('</tr>\n')
            # list plot
            f_http.write('<tr>\n')
            if (plot_movies == 'true'):
                if movie['plotoutline'] != "":
                    f_http.write('<td colspan="6">'+movie['plotoutline']+'</td>\n')
                else:
                    f_http.write('<td colspan="6">'+movie['plot']+'</td>\n')
            f_http.write('</tr>\n')
            moviecount += 1
            pDialog.update(int(float(moviecount * 100) / len(movies)), message=movie['label'])
        f_http.write('</table>\n')
        xbmc.sleep(200)
        pDialog.close()

    if (include_tvshows == 'true') and xbmc.getCondVisibility("Library.HasContent(TVShows)"):
        f_http.write('<a class="anchor" id="tvshow_link">anchor</a>\n')
        f_http.write('<table class="gridtable">\n')
        f_http.write('<tr>\n')
        f_http.write('<th colspan="6"><span style="text-transform: uppercase">'+xbmc.getLocalizedString(20343)+':</span> ('+str(len(tvshows))+') <span style="text-transform: uppercase">'+xbmc.getLocalizedString(20360)+':</span> ('+str(len(episodes))+')</th>\n')
        f_http.write('</tr>\n')
        pDialog.create(LANGUAGE(30033), '')
        tvcount = 0
        for tvshow in tvshows:
            tvgenre = " / ".join(tvshow['genre'])
            tvstudio = " / ".join(tvshow['studio'])
            tv_rating = str(round(float(tvshow['rating']),1))
            hd_episodes = 0
            sd_episodes = 0
            HD_Show = False
            for episode in episodes:
                if episode['streamdetails']['video'] != []:
                    videowidth = episode['streamdetails']['video'][0]['width']
                    videoheight = episode['streamdetails']['video'][0]['height']
                    if episode['tvshowid'] == tvshow['tvshowid']:
                        if videowidth >= 1280 or videoheight >= 720:
                            hd_episodes += 1
                        else:
                            sd_episodes += 1
            if round(float(hd_episodes),1) >= round(float((hd_episodes + sd_episodes) * 0.6),1):
                HD_Show = True
            f_http.write('<tr class="table";>\n')
            f_http.write('<td width="30%">\n')
            f_http.write('<div style="float:left;width:95%;"><b><a href="http://thetvdb.com/?tab=series&amp;id=' + str(tvshow['imdbnumber']) + '/" target="_blank">' + tvshow['label']+'</a></b> ('+str(tvshow['year'])+')</div>\n')
            if HD_Show == True:
                f_http.write('<div style="float:right;width:5%;"><img src="images/hd.png" alt="HD" width="24" height="15"</div>\n')
            else:
                f_http.write('<div style="float:right;width:5%;"><img src="images/sd.png" alt="SD" width="24" height="15"</div>\n')
            f_http.write('</td>\n')
            f_http.write('<td width="4%" align="center">'+str(tv_rating)+' &#9733;</td>\n')
            f_http.write('<td width="30%">'+str(tvgenre)+'</td>\n')
            f_http.write('<td width="15%">'+tvstudio+'</td>\n')
            f_http.write('<td width="12%">'+xbmc.getLocalizedString(33054)+' '+str(tvshow['season'])+' / '+xbmc.getLocalizedString(20360)+' '+str(tvshow['episode'])+'</td>\n')
            # format tvshow mpaa
            if str(tvshow['mpaa']) == "":
                f_http.write('<td>'+LANGUAGE(30014)+' NA</td>\n')
            else:
                f_http.write('<td>'+LANGUAGE(30014)+' '+str(tvshow['mpaa'])+'</td>\n')
            f_http.write('</tr>\n')
            f_http.write('<tr>\n')
            # list plot
            if (plot_tvshows == 'true'):
                f_http.write('<td colspan="6">'+tvshow['plot']+'</td>\n')
            f_http.write('</tr>\n')
            tvcount += 1
            pDialog.update(int(float(tvcount * 100) / len(tvshows)), message=tvshow['label'])
        f_http.write('</table>\n')
        xbmc.sleep(200)
        pDialog.close()

    f_http.write('</div>\n')
    f_http.write('<div id="footer">\n')
    f_http.write('<hr width="90%">\n')
    f_http.write('<div style="float:right;padding-right:5.5%;padding-bottom:10px;">\n')
    f_http.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;">'+LANGUAGE(30030)+'<a href="https://github.com/Steveb1968/script.html.library-report" target="_blank">script.html.library-report</a> by Steveb</p>\n')
    f_http.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;float:right;">'+LANGUAGE(30015)+'<a href="http://forum.xbmc.org/showthread.php?tid=167632" target="_blank">script.html.library-report</a></p>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('</body>\n')
    f_http.write('</html>')
    f_http.close()
    if (enable_ftp == 'false'):
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (ADDON_NAME, LANGUAGE(30005), 4000, ICON))
    else:
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30005), LANGUAGE(30006), 4000, ICON))


def copy_files_local():
    for f in data_files:
        full_file_name = os.path.join(DATA, f)
        if f == 'password_protect.php':
            pass
        else:
            shutil.copy(full_file_name, file_path)

    if not os.path.exists(image_dest):
        os.makedirs(image_dest)

    for f in image_files:
        full_file_name = os.path.join(IMAGE, f)
        if not(os.path.isfile(image_dest + '/' + f)):
            shutil.copy(full_file_name, image_dest)


def password_protect():
    php_data = ""
    password_php = xbmc.translatePath(os.path.join(DATA, 'password_protect.php').encode("utf-8")).decode("utf-8")
    with codecs.open(password_php, "r", encoding="utf-8") as file:
        data = file.readlines()
    # change the selected lines
    data[51] = "\t'"+web_password+"'\n"
    data[58] = "define('LOGOUT_URL', 'http://"+logout+"/');\n"
    # write back
    with codecs.open(password_php, "w", encoding="utf-8") as file:
        file.writelines(data)
        file.close()

    try:
        if not (web_root == ""):
            if (change_ftp_dir == 'true') and directory != "":
                php_data = urllib2.urlopen("http://"+host+"/"+web_root+"/"+directory+"/password_protect.php?help", timeout = 5).read()
            else:
                php_data = urllib2.urlopen("http://"+host+"/"+web_root+"/password_protect.php?help", timeout = 5).read()
        else:
            if (change_ftp_dir == 'true') and directory != "":
                php_data = urllib2.urlopen("http://"+host+"/"+user+"/"+directory+"/password_protect.php?help", timeout = 5).read()
            else:
                php_data = urllib2.urlopen("http://"+host+"/"+user+"/password_protect.php?help", timeout = 5).read()
    except urllib2.URLError, e:
        xbmc.log(ADDON_NAME+": ## PHP HEADER ERROR "+str(e.code))
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30032),e, 4000, ICON))

    php_data = php_data.split('"', 1)[-1].split('"')[0]

    with codecs.open(str(file_path)+str(file_name), "r", encoding="utf-8") as file:
        data = file.readlines()
    # change the selected line
    data[0] = '<?php include("'+php_data+'"); ?>\n'
    xbmc.log(ADDON_NAME+": ## PHP HEADER DATA: "+data[0])
    # write back
    with codecs.open(str(file_path)+str(file_name), "w", encoding="utf-8") as file:
        file.writelines(data)
        file.close()

# ftp file transfer
def ftp():
    def chdir(session, directory):
        ch_dir_rec(session,directory.split('/'))
    # Check if directory exists (in current location)
    def directory_exists(session, directory):
        dirlist = []
        session.retrlines('LIST',dirlist.append)
        for f in dirlist:
            if f.split()[-1] == directory:
                return True
        return False
    def ch_dir_rec(session, descending_path_split):
        if len(descending_path_split) == 0:
            return
        next_level_directory = descending_path_split.pop(0)
        if not directory_exists(session,next_level_directory):
            session.mkd(next_level_directory)
        session.cwd(next_level_directory)
        ch_dir_rec(session,descending_path_split)

    def php_upload():
        try:
            session = ftplib.FTP(host,user,password)
            if (change_ftp_dir == 'true') and directory != "":
                chdir(session, directory)
            if not "password_protect.php" in session.nlst():
                for f in data_files:
                    if (f == "password_protect.php"):
                        file = open(os.path.join(DATA, f),'rb')
                        session.storlines('STOR ' + f, file)
                        file.close()
            else:
                pass
        except Exception,e:
            xbmc.sleep(200)
            xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30026),e, 4000, ICON))

    def ftp_files():
        file = open(str(file_path)+str(file_name),'rb')
        session.storlines('STOR ' + str('index.php'), file)
        file.close()
        for f in data_files:
            file = open(os.path.join(DATA, f),'rb')
            session.storlines('STOR ' + f, file)
            file.close()
        if (enable_password == 'false') and 'password_protect.php' in session.nlst():
            session.delete('password_protect.php')
        if not 'images' in session.nlst():
            session.mkd('images')
        session.cwd('images')
        for f in image_files:
            if not f in session.nlst():
                file = open(os.path.join(IMAGE, f),'rb')
                session.storbinary('STOR ' + f, file)
                file.close()

    try:
        pDialog.create(ADDON_NAME, '')
        pDialog.update(0, message=LANGUAGE(30006))
        session = ftplib.FTP(host,user,password)
        pDialog.update(25, message=LANGUAGE(30006))
        if (change_ftp_dir == 'true') and directory != "":
            chdir(session, directory)
            pDialog.update(30, message=LANGUAGE(30006))
        if (enable_password == 'true'):
            php_upload()
            pDialog.update(40, message=LANGUAGE(30006))
            password_protect()
            pDialog.update(50, message=LANGUAGE(30006))
        ftp_files()
        pDialog.update(100, message=LANGUAGE(30006))
        session.quit()
        xbmc.sleep(200)
        pDialog.close()
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (ADDON_NAME,LANGUAGE(30025), 4000, ICON))
    except Exception,e:
        session.quit()
        pDialog.close()
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30026),e, 4000, ICON))

if (__name__ == "__main__"):
    xbmc.log(ADDON_NAME+": ## STARTED")
    main()
    if (enable_ftp == 'true'):
        xbmc.log(ADDON_NAME+": ## UPLOADING TO FTP HOST")
        ftp()
    copy_files_local()
    xbmc.log(ADDON_NAME+": ## FINISHED")