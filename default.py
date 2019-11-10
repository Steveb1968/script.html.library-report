#!/usr/bin/python

import os
import xbmc
import xbmcgui
import xbmcaddon
import time
import ftplib
import json
import codecs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
LANGUAGE = ADDON.getLocalizedString
ICON = ADDON.getAddonInfo('icon')
DEFAULT_DATA = xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8')

file_path = ADDON.getSetting('save_location')
include_movies = ADDON.getSetting('includemovies')
include_tvshows = ADDON.getSetting('includetvshows')
enable_ftp = ADDON.getSetting('Enable_ftp')
host = ADDON.getSetting('server')
user = ADDON.getSetting('user')
password = ADDON.getSetting('password')
change_ftp_dir = ADDON.getSetting('enable_ftp_dir')
ftp_directory = ADDON.getSetting('ftp_dir')

if file_path == "Default (userdata/addon_data)":
    if not os.path.exists(DEFAULT_DATA):
        os.makedirs(DEFAULT_DATA)
    file_path = DEFAULT_DATA

pDialog = xbmcgui.DialogProgressBG()
pDialog.create(ADDON_NAME, '')
pDialog.update(0, message = LANGUAGE(30034))

if (include_movies == 'true') and xbmc.getCondVisibility("Library.HasContent(Movies)"):
    command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties" : ["genre", "studio", "rating", "year", "mpaa", "imdbnumber", "streamdetails", "runtime", "playcount"], "sort": { "order": "ascending", "method": "title", "ignorearticle": true } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    movies = jsonobject["result"]["movies"]
    pDialog.update(50, message=LANGUAGE(30034))

if (include_tvshows == 'true') and xbmc.getCondVisibility("Library.HasContent(TVShows)"):
    command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["genre", "title", "studio", "season", "episode", "rating", "year", "mpaa", "imdbnumber", "runtime", "playcount"], "sort": { "order": "ascending", "method": "title" } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    tvshows = jsonobject["result"]["tvshows"]
    pDialog.update(75, message=LANGUAGE(30034))

    command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["tvshowid", "episode", "season", "streamdetails"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
    result = xbmc.executeJSONRPC(command)
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = json.loads(result)
    episodes = jsonobject["result"]["episodes"]
    pDialog.update(100, message=LANGUAGE(30034))

xbmc.sleep(200)
pDialog.close()

def main():
    f_http = codecs.open(os.path.join(file_path, 'index.html'), "w", encoding="utf-8")
    f_http.write('<!DOCTYPE html>\n')
    f_http.write('<head>\n')
    f_http.write('<meta content="text/html; charset=UTF-8" http-equiv="Content-Type">\n')
    f_http.write('<title>' + ADDON_NAME + '</title>\n')
    f_http.write('<style>\n')
    f_http.write('body {background-color:#333333; margin:0; padding:0}\n')
    f_http.write('h1 {color:DeepSkyBlue; text-align:center; margin-top: 0.42em; font-family:Arial Black; text-transform:uppercase}\n')
    f_http.write('p.date {color:white; margin:0; padding-top:12px; text-align:right; font-family:Arial}\n')
    f_http.write('table.gridtable {font-family:Arial; font-size:14.5px; border-width:1px; border-color:Black; border-collapse:collapse; width:98%; margin:auto}\n')
    f_http.write('table.gridtable th {font-size:20px; font-family:Arial Black; text-transform: uppercase; border-width:1px; padding:8px; border-style:solid; border-color:Black; background-color:Silver}\n')
    f_http.write('table.gridtable td {border-width:1px; padding:8px; border-style:solid; border-color:Black; background-color:White}\n')
    f_http.write('a.anchor{display: block; position:relative; top:-60px; visibility: hidden}\n')
    f_http.write('a:link {color:Black} a:visited {color:Black} a:hover {color:Black} a:active {color:Black} a:hover {background:White} a:focus {outline:none}\n')
    f_http.write('.github a:link {color:DeepSkyBlue} .github a:visited {color:DeepSkyBlue} .github a:hover {color:YellowGreen} .github a:active {color:YellowGreen} .github a:hover {background:none}\n')
    f_http.write('.button {display:inline-block; font-weight:bold; font-size:15px; width:110px; height:20px; background:Silver; padding-top:3.5px; text-align:center; border-radius:4px; text-transform:uppercase; text-decoration:none; font-family:Arial}\n')
    f_http.write('.res {font-style:italic; font-family:Arial Black;font-size:13px; margin:0}\n')
    f_http.write('</style>\n')
    f_http.write("</head>\n")
    f_http.write('<body>\n')
    f_http.write('<div id="header" style="height:80px; width:100%; position:fixed; background-color:#333333">\n')
    f_http.write('<div id="Date" style="height:80px; width:25%; float:right; padding-right:1.5%">\n')
    f_http.write('<p class="date">' + LANGUAGE(30012) + time.strftime('%d %B %Y') + '</p>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Links" style="height:80px; width:25%; float:left; padding-left:1.5%; padding-top:13px">\n')
    if (include_movies == 'true') and (include_tvshows == 'true'):
        f_http.write('<a href="#movie_link" class="button">' + xbmc.getLocalizedString(342) + '</a>&nbsp;&nbsp;<a href="#tvshow_link" class="button">' + xbmc.getLocalizedString(20343) + '</a>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Heading" style="height:80px; width:50%; margin-left:auto; margin-right:auto">\n')
    f_http.write('<h1>' + ADDON_NAME + '</h1>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Body" style="width:100%; padding-top:60px">\n')
    if (include_movies == 'true') and xbmc.getCondVisibility("Library.HasContent(Movies)"):
        f_http.write('<a class="anchor" id="movie_link">anchor</a>\n')
        f_http.write('<table class="gridtable">\n')
        f_http.write('<tr>\n')
        f_http.write('<th colspan="8">' + xbmc.getLocalizedString(342) + ' (' + '{:,}'.format(len(movies)) + ')</th>\n')
        f_http.write('</tr>\n')
        pDialog.create(LANGUAGE(30033), '')
        moviecount = 0
        for movie in movies:
            moviegenre = " / ".join(movie['genre'])
            moviestudio = " / ".join(movie['studio'])
            movie_rating = round(float(movie['rating']), 1)
            movie_runtime = '%i min' % int(movie['runtime'] / 60)
            if movie['streamdetails']['video'] != []:
                videowidth = movie['streamdetails']['video'][0]['width']
                videoheight = movie['streamdetails']['video'][0]['height']
                if videowidth > 4096 or videoheight > 2160:
                    videoresolution = '<td width="2.5%" align="center" class="res" style="color:DarkGoldenRod">8K</td>\n'
                elif videowidth > 1920 or videoheight > 1080:
                    videoresolution = '<td width="2.5%" align="center" class="res" style="color:DarkGoldenRod">4K</td>\n'
                elif videowidth >= 1280 or videoheight >= 720:
                    videoresolution = '<td width="2.5%" align="center" class="res" style="color:DodgerBlue">HD</td>\n'
                else:
                    videoresolution = '<td width="2.5%" align="center" class="res" style="color:DimGrey">SD</td>\n'
            if movie['playcount'] > 0:
                watched = '&#x2714;'
            else:
                watched = ''
            f_http.write('<tr>\n')
            f_http.write('<td width="27.5%"><b><a href="http://www.imdb.com/title/' + str(movie['imdbnumber']) + '/" target="_blank">' + movie['label'] + '</a></b> (' + str(movie['year']) + ')</td>\n')
            f_http.write(videoresolution)
            f_http.write('<td width="4%" align="center">' + str(movie_rating) + ' &#9733;' + '</td>\n')
            f_http.write('<td width="5%" align="center">' + str(movie_runtime) + '</td>\n')
            f_http.write('<td width="25.5%">' + moviegenre + '</td>\n')
            f_http.write('<td width="25.5%">' + moviestudio + '</td>\n')
            if movie['mpaa'].startswith(LANGUAGE(30014)):
                f_http.write('<td width="8%">' + movie['mpaa'] + '</td>\n')
            elif movie['mpaa'] == "":
                f_http.write('<td width="8%">' + LANGUAGE(30014) + ' NA</td>\n')
            else:
                f_http.write('<td width="8%">' + LANGUAGE(30014) + ' ' + movie['mpaa'] + '</td>\n')
            f_http.write('<td align="center">' + watched + '</td>\n')
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
        f_http.write('<th colspan="9">' + xbmc.getLocalizedString(20343 ) + ' (' + '{:,}'.format(len(tvshows)) + ') - ' + xbmc.getLocalizedString(20360) + ' (' + '{:,}'.format(len(episodes)) + ')</th>\n')
        f_http.write('</tr>\n')
        pDialog.create(LANGUAGE(30033), '')
        tvcount = 0
        for tvshow in tvshows:
            tvgenre = " / ".join(tvshow['genre'])
            tvstudio = " / ".join(tvshow['studio'])
            tv_rating = round(float(tvshow['rating']), 1)
            tv_runtime = '%i min' % int(tvshow['runtime'] / 60)
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
            if round(float(hd_episodes), 1) >= round(float((hd_episodes + sd_episodes) * 0.6), 1):
                HD_Show = True
            if tvshow['playcount'] > 0:
                watched = '&#x2714;'
            else:
                watched = ''
            f_http.write('<tr>\n')
            f_http.write('<td width="27.5%"><b><a href="http://thetvdb.com/?tab=series&amp;id=' + str(tvshow['imdbnumber']) + '/" target="_blank">' + tvshow['label'] + '</a></b> (' + str(tvshow['year']) + ')</td>\n')
            if HD_Show == True:
                f_http.write('<td width="2.5%" align="center" class="res" style="color:DodgerBlue">HD</td>\n')
            else:
                f_http.write('<td width="2.5%" align="center" class="res" style="color:DimGrey">SD</td>\n')
            f_http.write('<td width="4%" align="center">' + str(tv_rating) + ' &#9733;</td>\n')
            f_http.write('<td width="5%" align="center">' + str(tv_runtime) + '</td>\n')
            f_http.write('<td width="25.5%">' + tvgenre + '</td>\n')
            f_http.write('<td width="12.5%">' + tvstudio + '</td>\n')
            f_http.write('<td width="13%">' + xbmc.getLocalizedString(33054) + ' ' + str(tvshow['season']) + ' / ' + xbmc.getLocalizedString(20360) + ' ' + str(tvshow['episode']) + '</td>\n')
            if tvshow['mpaa'] == "":
                f_http.write('<td width="8%">' + LANGUAGE(30014) + ' NA</td>\n')
            else:
                f_http.write('<td width="8%">' + LANGUAGE(30014) + ' ' + tvshow['mpaa'] + '</td>\n')
            f_http.write('<td align="center">' + watched + '</td>\n')
            f_http.write('</tr>\n')
            tvcount += 1
            pDialog.update(int(float(tvcount * 100) / len(tvshows)), message=tvshow['label'])
        f_http.write('</table>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="footer">\n')
    f_http.write('<hr width="98%">\n')
    f_http.write('<div style="float:right; padding-right:1.5%; padding-bottom:12px">\n')
    f_http.write('<p class="github" style="color:white; font-family:Arial; margin:0">GitHub: <a href="https://github.com/Steveb1968/script.html.library-report" target="_blank">' + ADDON_ID + '</a></p>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('</body>\n')
    f_http.write('</html>')
    f_http.close()
    pDialog.close()
    if (enable_ftp == 'false'):
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (ADDON_NAME, LANGUAGE(30005), 4500, ICON))
    else:
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30005), LANGUAGE(30006), 4500, ICON))

def ftp():
    session = ftplib.FTP(host,user,password)

    def chdir(session, ftp_directory):
        ch_dir_rec(session, ftp_directory.split('/'))

    def directory_exists(session, ftp_directory):
        dirlist = []
        session.retrlines('LIST', dirlist.append)
        for f in dirlist:
            if f.split()[-1] == ftp_directory:
                return True
        return False

    def ch_dir_rec(session, descending_path_split):
        if len(descending_path_split) == 0:
            return
        next_level_directory = descending_path_split.pop(0)
        if not directory_exists(session, next_level_directory):
            session.mkd(next_level_directory)
        session.cwd(next_level_directory)
        ch_dir_rec(session, descending_path_split)

    try:
        pDialog.create(ADDON_NAME, '')
        pDialog.update(0, message=LANGUAGE(30006))
        session = ftplib.FTP(host,user,password)
        pDialog.update(25, message=LANGUAGE(30006))
        if (change_ftp_dir == 'true') and ftp_directory != "":
            chdir(session, ftp_directory)
        file = open(file_path + 'index.html', 'rb')
        session.storlines('STOR ' + 'index.html', file)
        file.close()
        pDialog.update(50, message=LANGUAGE(30006))
        session.quit()
        pDialog.update(100, message=LANGUAGE(30006))
        xbmc.sleep(200)
        pDialog.close()
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (ADDON_NAME, LANGUAGE(30025), 4500, ICON))
    except Exception, e:
        session.quit()
        pDialog.close()
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification(%s, %s, %d, %s)" % (LANGUAGE(30026), e, 4500, ICON))


if (__name__ == "__main__"):
    main()
    if (enable_ftp == 'true'):
        ftp()
