import os, sys
import xbmc, xbmcgui, xbmcaddon
import time
import codecs, shutil
import ftplib
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__     = xbmcaddon.Addon(id='script.html.library-report')
__addonname__ = __addon__.getAddonInfo('name')
__language__  = __addon__.getLocalizedString
__icon__      = __addon__.getAddonInfo('icon')
__cwd__       = __addon__.getAddonInfo('path').decode("utf-8")
__resource__  = xbmc.translatePath( os.path.join( __cwd__, 'resources' ).encode("utf-8") ).decode("utf-8")
__data__      = xbmc.translatePath( os.path.join( __resource__, 'data' ).encode("utf-8") ).decode("utf-8")
__image__     = xbmc.translatePath( os.path.join( __resource__, 'images' ).encode("utf-8") ).decode("utf-8")

# get addon settings
file_path = __addon__.getSetting('save_location') 
enable_password = __addon__.getSetting('Enable_Password')
include_movies = __addon__.getSetting('includemovies')
plot_movies = __addon__.getSetting('movieplot')
include_tvshows = __addon__.getSetting('includetvshows')
plot_tvshows = __addon__.getSetting('tvshowplot')
list_episodes = __addon__.getSetting('episodes')
enable_ftp = __addon__.getSetting('Enable_ftp')
host = __addon__.getSetting('server')
user = __addon__.getSetting('user')
password = __addon__.getSetting('password')
change_ftp_dir = __addon__.getSetting('enable_ftp_dir')
directory = __addon__.getSetting('ftp_dir')
web_password = __addon__.getSetting('web_password')
logout = __addon__.getSetting('logout_url')
session = ftplib.FTP(host,user,password)
image_files = os.listdir(__image__)

# file locations/names & paths
while file_path=="":
    xbmcgui.Dialog().ok(__addonname__,__language__(30004))
    __addon__.openSettings()
    file_path = __addon__.getSetting('save_location')

file_name = 'index.html'
data_files = os.listdir(__data__)
image_files = os.listdir(__image__)
image_dest = os.path.join(file_path, 'images')
f_http = codecs.open(os.path.join(file_path,str(file_name)), "w", encoding="utf-8")

LIST_TYPE = {}
LIST_TYPE['0'] = 'basic'
LIST_TYPE['1'] = 'table'
list_output = LIST_TYPE[__addon__.getSetting('listtype')]

xbmc.executebuiltin( "ActivateWindow(busydialog)" )

# data
if (include_movies == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties" : ["genre", "studio", "plotoutline", "plot", "rating", "year", "mpaa", "imdbnumber", "streamdetails", "top250", "runtime"], "sort": { "order": "ascending", "method": "title", "ignorearticle": true } }, "id": 1}'
    result = xbmc.executeJSONRPC( command )
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = simplejson.loads(result)
    movies = jsonobject["result"]["movies"]
    top250count = 0
    for movie in movies:
        if int(movie['top250']) > 0:
            top250count += 1

if (include_tvshows == 'true') and xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["genre", "title", "studio", "premiered", "plot", "rating", "year", "mpaa", "imdbnumber"], "sort": { "order": "ascending", "method": "title" } }, "id": 1}'
    result = xbmc.executeJSONRPC( command )
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = simplejson.loads(result)
    tvshows = jsonobject["result"]["tvshows"]

    command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["tvshowid", "episode", "season", "streamdetails", "runtime"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
    result = xbmc.executeJSONRPC( command )
    result = unicode(result, 'utf-8', errors='ignore')
    jsonobject = simplejson.loads(result)
    episodes = jsonobject["result"]["episodes"]

# create html output
def html():
    # password_protect
    if (enable_password == 'true'):
        f_http.write('\n')
    f_http.write('<!DOCTYPE html>\n')
    f_http.write('<head>\n')
    f_http.write('<meta  content="text/html;  charset=UTF-8"  http-equiv="Content-Type">\n')
    f_http.write('<link rel="shortcut icon" href="images/favicon.ico">\n')
    f_http.write('<link rel="icon" sizes="16x16 32x32 64x64" href="images/favicon.ico">\n')
    f_http.write('<title>Kodi '+__language__(30007)+'</title>\n')
    f_http.write('<link rel="stylesheet" href="Default.css">\n') 
    f_http.write('<script language="JavaScript" charset="UTF-8" src="SearchScript.js"></script>\n')
    f_http.write("</head>\n")
    f_http.write('<body background="images/bg.png">\n')
    f_http.write('<div id="header" style="height:95px;width:90%;position : fixed;background-color:#333333;margin-left: 5%;margin-right: auto ;">\n')
    f_http.write('<div id="Date" style="height:95px;width:20%;float:right;padding-right:1%;padding-top:15px;">\n')
    f_http.write('<p class="date">'+__language__(30012)+time.strftime('%d %B %Y')+'</p>\n')
    # password_protect logout
    if (enable_password == 'true'):
        f_http.write('<form style="float:right;padding-top:30px;" method="get" action="password_protect.php" /><input type="submit" value="Logout" /><input type="hidden" name="logout" value="1" /></form>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Search" style="height:95px;width:20%;float:left;padding-left:1%;padding-top:15px;">\n')
    f_http.write("<iframe id="+'"srchform2" '+'src="'+"javascript:'<html><body style=margin:0px;><form action="+"\\'javascript:void();\\' onSubmit=if(this.t1.value!=\\'\\')parent.findString(this.t1.value);return(false);><input type=text id=t1 name=t1 size=20><input type=submit name=b1 value=Find></form></body></html>'"+'"'+" width=220 height=34 border=0 frameborder=0 scrolling=no></iframe>\n")
    if (include_movies == 'true') and (include_tvshows == 'true'):
        f_http.write('<p class="links"><a href="#movie_link">'+xbmc.getLocalizedString(342)+' ('+str(len(movies))+')'+'</a>&nbsp;&nbsp;<a href="#tvshow_link">'+xbmc.getLocalizedString(20343)+' ('+str(len(tvshows))+')'+'</a></p>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Heading" style="height:95px;width:80%;margin-left: auto;margin-right: auto ;">\n')
    f_http.write('<h1><img src="images/logo.png" alt="Kodi" width="150" height="52" align="center"> '+__language__(30007)+'</h1>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('<div id="Body" style="width:100%;padding-top:75px;">\n')
    if (list_output == 'basic'):
        default_list()
    elif (list_output == 'table'):
        table_list()
    f_http.write('</div>\n')
    f_http.write('<div id="footer">\n')
    f_http.write('<hr width="90%">\n')
    f_http.write('<div style="float:right;padding-right:5.5%;padding-bottom:10px;">\n')
    f_http.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;">'+__language__(30030)+'<a href="https://github.com/Steveb1968/script.html.library-report" target="_blank">script.html.library-report</a> by Steveb</p>\n')
    f_http.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;float:right;">'+__language__(30015)+'<a href="http://forum.xbmc.org/showthread.php?tid=167632" target="_blank">script.html.library-report</a></p>\n')
    f_http.write('</div>\n')
    f_http.write('</div>\n')
    f_http.write('</body>\n')
    f_http.write('</html>')
    f_http.close()

def default_list():
    if (include_movies == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
        f_http.write('<a class="anchor" id="movie_link">anchor</a>\n')
        f_http.write('<hr width="90%">\n')
        f_http.write('<h2><span style="text-transform: uppercase">'+xbmc.getLocalizedString(342)+':</span> ('+str(len(movies))+' '+xbmc.getLocalizedString(20161)+' / '+str(top250count)+' '+__language__(30013)+')</h2>\n')
        f_http.write('<hr width="90%">\n')
        f_http.write('&nbsp;\n')
        for movie in movies:
            moviegenre = " / ".join(movie['genre'])
            moviestudio = " / ".join(movie['studio'])
            movie_rating = '<span style="color:white"> &bull; </span><span style="color:GoldenRod">'+str(round(float(movie['rating']),1))+' &#9733;</span>'
            movie_runtime = '<span style="color:white"> &bull; </span><span style="color:darkgrey">%s min</span>' % str(movie['runtime'] / 60)+'</span>' 
            if movie['streamdetails']['video'] != []:
                videowidth = movie['streamdetails']['video'][0]['width']
                videoheight = movie['streamdetails']['video'][0]['height']
                if videowidth <= 720 and videoheight <= 480:
                    videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                elif videowidth <= 768 and videoheight <= 576:
                    videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                elif videowidth <= 960 and videoheight <= 544:
                    videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                elif videowidth <= 1280 and videoheight <= 720:
                    videoresolution = '&nbsp;&nbsp;<img src="images/hd.png" alt="HD" width="24" height="15">'
                else:
                    videoresolution = '&nbsp;&nbsp;<img src="images/hd.png" alt="HD" width="24" height="15">'
            if movie['streamdetails']['audio'] != []:
                audiochannels = int(movie['streamdetails']['audio'][0]['channels'])
                if audiochannels == 8:
                    channels = '<img src="images/8ch.png" alt="7.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                elif audiochannels == 6:
                    channels = '<img src="images/6ch.png" alt="5.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                elif audiochannels == 4:
                    channels = '<img src="images/4ch.png" alt="4.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                elif audiochannels == 3:
                    channels = '<img src="images/3ch.png" alt="2.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                elif audiochannels == 2:
                    channels = '<img src="images/2ch.png" alt="2.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                elif audiochannels == 1:
                    channels = '<img src="images/1ch.png" alt="1.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                else:
                    channels = ''
            f_http.write('<p class="mediatitle">'+movie['label']+' ('+str(movie['year'])+')&nbsp;&nbsp;<a href="http://www.imdb.com/title/'+str(movie['imdbnumber'])+'/" target="_blank"><img src="images/imdb_logo.png" alt="IMDB" width="32" height="16" align="bottom"></a></p>\n')
            f_http.write('<p class="genre">'+str(moviegenre)+str(movie_rating))
            if int(movie['top250']) > 0:
                f_http.write('<span style="color:GoldenRod"> (#'+str(movie['top250'])+')</span>'+str(movie_runtime)+str(videoresolution)+str(channels)+'</p>\n')
            else:
                f_http.write(str(movie_runtime)+str(videoresolution)+str(channels)+'</p>\n')
            f_http.write('<p class="studio">'+moviestudio+'</p>\n')
            # format movie mpaa
            if str(movie['mpaa']).startswith(__language__(30014)):
                f_http.write('<p class="mpaa">'+str(movie['mpaa'])+'</p>\n')
            elif str(movie['mpaa']) == "":
                f_http.write('<p class="mpaa">'+__language__(30014)+' NA</p>\n')
            else:
                f_http.write('<p class="mpaa">'+__language__(30014)+' '+str(movie['mpaa'])+'</p>\n')
            # list plot
            if (plot_movies == 'true'):
                if movie['plotoutline'] != "":
                    f_http.write('<p class="plot">'+movie['plotoutline']+'</p>\n')
                else:
                    f_http.write('<p class="plot">'+movie['plot']+'</p>\n')
                f_http.write('&nbsp;\n')
                if movie != movies[-1]:
                    f_http.write('<hr width="90%">\n')
                    f_http.write('&nbsp;\n')
            else:
                f_http.write('&nbsp;\n')

    if (include_tvshows == 'true') and xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
        f_http.write('<a class="anchor" id="tvshow_link">anchor</a>\n')
        f_http.write('<hr width="90%">\n')
        f_http.write('<h2><span style="text-transform: uppercase">'+xbmc.getLocalizedString(20343)+':</span> ('+str(len(tvshows))+' '+xbmc.getLocalizedString(20161)+' / '+str(len(episodes))+' '+xbmc.getLocalizedString(20360)+')</h2>\n')
        f_http.write('<hr width="90%">\n')
        for tvshow in tvshows:
            tvgenre = " / ".join(tvshow['genre'])
            tvstudio = " / ".join(tvshow['studio'])
            tv_rating = str(round(float(tvshow['rating']),1))
            f_http.write('&nbsp;\n')
            f_http.write('<p class="mediatitle">' + tvshow['label']+' ('+str(tvshow['year'])+')&nbsp;&nbsp;<a href="http://thetvdb.com/?tab=series&amp;id=' + str(tvshow['imdbnumber']) + '/" target="_blank"><img src="images/tvdb_logo.png" alt="TVDB" width="32" height="16" align="bottom"></a></p>\n')
            episode_list = []
            for episode in episodes:
                episode_runtime = '<span style="color:white"> &bull; </span><span style="color:darkgrey">%s min' % str(episode['runtime'] / 60) +'</span>'
                if episode['streamdetails']['video'] != []:
                    videowidth = episode['streamdetails']['video'][0]['width']
                    videoheight = episode['streamdetails']['video'][0]['height']
                    if videowidth <= 720 and videoheight <= 480:
                        videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                    elif videowidth <= 768 and videoheight <= 576:
                        videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                    elif videowidth <= 960 and videoheight <= 544:
                        videoresolution = '&nbsp;&nbsp;<img src="images/sd.png" alt="SD" width="24" height="15">'
                    elif videowidth <= 1280 and videoheight <= 720:
                        videoresolution = '&nbsp;&nbsp;<img src="images/hd.png" alt="HD" width="24" height="15">'
                    else:
                        videoresolution = '&nbsp;&nbsp;<img src="images/hd.png" alt="HD" width="24" height="15">'
                if episode['streamdetails']['audio'] != []:
                    audiochannels = int(episode['streamdetails']['audio'][0]['channels'])
                    if audiochannels == 8:
                        channels = '<img src="images/8ch.png" alt="7.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    elif audiochannels == 6:
                        channels = '<img src="images/6ch.png" alt="5.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    elif audiochannels == 4:
                        channels = '<img src="images/4ch.png" alt="4.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    elif audiochannels == 3:
                        channels = '<img src="images/3ch.png" alt="2.1ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    elif audiochannels == 2:
                        channels = '<img src="images/2ch.png" alt="2.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    elif audiochannels == 1:
                        channels = '<img src="images/1ch.png" alt="1.0ch" width="40" height="16" style="PADDING-LEFT: 6px">'
                    else:
                        channels = ''
                if episode['tvshowid'] == tvshow['tvshowid']:
                    episode_list.append((episode['season'],episode['episode'],episode['label']+str(episode_runtime)+str(videoresolution)+str(channels)))
            prev_season = None
            seasoncount = 0
            for episode in episode_list:
                season = episode[0]
                if season != prev_season:
                    seasoncount += 1
                    prev_season = season            
            f_http.write('<p class="episodecount">('+xbmc.getLocalizedString(33054)+' ' +str(seasoncount)+' / '+str(len(episode_list))+' '+xbmc.getLocalizedString(20360)+')</p>\n')            
            f_http.write('<p class="genre">'+str(tvgenre)+'<span style="color:white"> &bull; </span><span style="color:GoldenRod">'+str(tv_rating)+' &#9733;</span></p>\n')
            f_http.write('<p class="studio">'+tvstudio+'</p>\n')
            # format tvshow mpaa
            if str(tvshow['mpaa']) == "":
                f_http.write('<p class="mpaa">'+__language__(30014)+' NA</p>\n')
            else:
                f_http.write('<p class="mpaa">'+__language__(30014)+' '+str(tvshow['mpaa'])+'</p>\n')
            # list plot
            if (plot_tvshows == 'true'):
                f_http.write('<p class="plot">'+tvshow['plot']+'</p>\n')
                if tvshow != tvshows[-1] and (list_episodes == 'false'):
                    f_http.write('&nbsp;\n')
                    f_http.write('<hr width="90%">\n')
                    f_http.write('&nbsp;\n')
            # list episodes
            if (list_episodes == 'true'):
                prev_season = None
                for episode in episode_list:
                    season = episode[0]
                    if season != prev_season:
                        f_http.write('<h3>'+xbmc.getLocalizedString(20373)+' '+str(season)+'</h3>\n')
                        prev_season = season
                    f_http.write('<p class="episode">'+episode[2]+'</p>\n')
                f_http.write('&nbsp;\n')
                if tvshow != tvshows[-1]:
                    f_http.write('<hr width="90%">\n')
        f_http.write('&nbsp;\n')

def table_list():
    if (include_movies == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
        f_http.write('<a class="anchor" id="movie_link">anchor</a>\n')
        f_http.write('<table class="gridtable">\n')
        f_http.write('<tr>\n')
        f_http.write('<th colspan="6"><span style="text-transform: uppercase">'+xbmc.getLocalizedString(342)+':</span> ('+str(len(movies))+' '+xbmc.getLocalizedString(20161)+' / '+str(top250count)+' '+__language__(30013)+')</th>\n')
        f_http.write('</tr>\n')
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
            if str(movie['mpaa']).startswith(__language__(30014)):
                f_http.write('<td>'+str(movie['mpaa'])+'</td>\n')
            elif str(movie['mpaa']) == "":
                f_http.write('<td>'+__language__(30014)+' NA</td>\n')
            else:
                f_http.write('<td>'+__language__(30014)+' '+str(movie['mpaa'])+'</td>\n')
            f_http.write('</tr>\n')
            # list plot
            f_http.write('<tr>\n')
            if (plot_movies == 'true'):
                if movie['plotoutline'] != "":
                    f_http.write('<td colspan="6">'+movie['plotoutline']+'</td>\n')
                else:
                    f_http.write('<td colspan="6">'+movie['plot']+'</td>\n')
            f_http.write('</tr>\n')
        f_http.write('</table>\n')

    if (include_tvshows == 'true') and xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
        f_http.write('<a class="anchor" id="tvshow_link">anchor</a>\n')
        f_http.write('<table class="gridtable">\n')
        f_http.write('<tr>\n')
        f_http.write('<th colspan="6"><span style="text-transform: uppercase">'+xbmc.getLocalizedString(20343)+':</span> ('+str(len(tvshows))+' '+xbmc.getLocalizedString(20161)+' / '+str(len(episodes))+' '+xbmc.getLocalizedString(20360)+')</th>\n')
        f_http.write('</tr>\n')
        for tvshow in tvshows:
            tvgenre = " / ".join(tvshow['genre'])
            tvstudio = " / ".join(tvshow['studio'])
            tv_rating = str(round(float(tvshow['rating']),1))
            tv_prem = tvshow['premiered']
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
            if round(float(hd_episodes),1) > round(float((hd_episodes + sd_episodes) * 0.6),1):
                HD_Show = True
            f_http.write('<tr class="table";>\n')
            f_http.write('<td width="30%">\n')
            f_http.write('<div style="float:left;width:95%;"><b><a href="http://thetvdb.com/?tab=series&amp;id=' + str(tvshow['imdbnumber']) + '/" target="_blank">' + tvshow['label']+'</a></b></div>\n')            
            if HD_Show == True:
                f_http.write('<div style="float:right;width:5%;"><img src="images/hd.png" alt="HD" width="24" height="15"</div>\n')
            else:
                f_http.write('<div style="float:right;width:5%;"><img src="images/sd.png" alt="SD" width="24" height="15"</div>\n')
            f_http.write('</td>\n')
            f_http.write('<td width="4%" align="center">'+str(tv_rating)+' &#9733;</td>\n')
            f_http.write('<td width="30%">'+str(tvgenre)+'</td>\n')
            f_http.write('<td width="15%">'+tvstudio+'</td>\n')
            f_http.write('<td width="10%">'+tv_prem+'</td>\n')
            # format tvshow mpaa
            if str(tvshow['mpaa']) == "":
                f_http.write('<td>'+__language__(30014)+' NA</td>\n')
            else:
                f_http.write('<td>'+__language__(30014)+' '+str(tvshow['mpaa'])+'</td>\n')
            f_http.write('</tr>\n')
            f_http.write('<tr>\n')
            # list plot
            if (plot_tvshows == 'true'):
                f_http.write('<td colspan="6">'+tvshow['plot']+'</td>\n')
            f_http.write('</tr>\n')
        f_http.write('</table>\n')

if (enable_ftp == 'false'):
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )
    xbmc.sleep(200)
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addonname__, __language__(30005), 4000, __icon__) )
else:
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ( __language__(30005), __language__(30006), 4000, __icon__) )

def copy_files_local():
    for f in data_files:
        full_file_name = os.path.join(__data__, f)
        if f == 'password_protect.php':
            pass
        else:
            shutil.copy(full_file_name, file_path)

    if not os.path.exists(image_dest):
        os.makedirs(image_dest)

    for f in image_files:
        full_file_name = os.path.join(__image__, f)
        if not(os.path.isfile(image_dest + '/' + f)):
            shutil.copy(full_file_name, image_dest)


def password_protect():
    password_php = xbmc.translatePath( os.path.join( __data__, 'password_protect.php' ).encode("utf-8") ).decode("utf-8")
    with codecs.open(password_php, "r", encoding="utf-8") as file:
        data = file.readlines()
    # change the selected lines
    data[51] = "\t'"+web_password+"'\n"
    data[58] = "define('LOGOUT_URL', 'http://"+logout+"/');\n"
    # write back
    with codecs.open(password_php, "w", encoding="utf-8") as file:
        file.writelines(data)
        file.close()

    with codecs.open(str(file_path)+str(file_name), "r", encoding="utf-8") as file:
        data = file.readlines()
    # change the selected line
    if (change_ftp_dir == 'true') and directory != "":
        data[0] = '<?php include("/data/www/'+host+'/'+user+'/'+directory+'/password_protect.php"); ?>\n'
    else:
        data[0] = '<?php include("/data/www/'+host+'/'+user+'/password_protect.php"); ?>\n'
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

    def ftp_files():
        file = open(str(file_path)+str(file_name),'rb')
        session.storlines('STOR ' + str('index.php'), file)
        file.close()
        for f in data_files:
            file = open( os.path.join( __data__, f ),'rb')
            session.storlines('STOR ' + f, file)
            file.close()
        if (enable_password == 'false') and 'password_protect.php' in session.nlst():
            session.delete('password_protect.php')
        if not 'images' in session.nlst():
            session.mkd('images')
        session.cwd('images')
        for f in image_files:
            if not f in session.nlst():
                file = open( os.path.join( __image__, f ),'rb')
                session.storbinary('STOR ' + f, file)
                file.close()

    try:
        if (change_ftp_dir == 'true') and directory != "":
            chdir(session, directory)
        ftp_files()
        session.quit()
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addonname__,__language__(30025), 4000, __icon__) )
    except Exception,e:
        xbmc.executebuiltin( "Dialog.Close(busydialog)" )
        xbmc.sleep(200)
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__language__(30026),e, 4000, __icon__) )

if ( __name__ == "__main__" ):
    xbmc.log(__addonname__+": ## STARTED")
    html()
    if (enable_password == 'true'):
        password_protect()
    if (enable_ftp == 'true'):
        xbmc.log(__addonname__+": ## UPLOADING TO FTP HOST")
        ftp()
    copy_files_local()
    xbmc.log(__addonname__+": ## FINISHED")