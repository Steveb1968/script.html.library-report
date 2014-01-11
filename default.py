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
__language__  = __addon__.getLocalizedString
__icon__      = __addon__.getAddonInfo('icon')
__cwd__       = __addon__.getAddonInfo('path').decode("utf-8")
__resource__  = xbmc.translatePath( os.path.join( __cwd__, 'resources' ).encode("utf-8") ).decode("utf-8")
__files__     = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'files' ).encode("utf-8") ).decode("utf-8")
	
# save path
file_path = __addon__.getSetting('save_location')
while file_path=="":
	xbmcgui.Dialog().ok(__addon__.getAddonInfo('name'),__language__(30004))
	__addon__.openSettings()
	file_path = __addon__.getSetting('save_location')
	
xbmc.executebuiltin( "ActivateWindow(busydialog)" )

# file name	
if (__addon__.getSetting('Enable_Password') == 'true'):
	file_name = 'index.php'
	password_file = 'password_protect.php'
else:
	file_name = 'index.html'


# sort order	
sort_by = {}
sort_by['0'] = 'title'            
sort_by['1'] = 'year'          
sort_by['2'] = 'rating'            
sort_by['3'] = 'dateadded'
MovieSortBy = str(sort_by[__addon__.getSetting('msort_by')])
TvSortBy = str(sort_by[__addon__.getSetting('tsort_by')])

sort = {}
sort['0'] = 'ascending'            
sort['1'] = 'descending'
MovieSort = str(sort[__addon__.getSetting('msort_mode')])        
TvSort = str(sort[__addon__.getSetting('tsort_mode')])

directory = __addon__.getSetting('ftp_dir')
top250count = 0

# data
if (__addon__.getSetting('includemovies') == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties" : ["genre", "plotoutline", "plot", "rating", "year", "mpaa", "imdbnumber", "streamdetails", "top250", "runtime"], "sort": { "order": "'+MovieSort+'", "method": "'+MovieSortBy+'", "ignorearticle": true } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	movies = jsonobject["result"]["movies"]	
	for movie in movies:
		if int(movie['top250']) > 0:
			top250count += 1

if (__addon__.getSetting('includetvshows') == 'true') and xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["genre", "title", "plot", "rating", "originaltitle", "year", "mpaa", "imdbnumber"], "sort": { "order": "'+TvSort+'", "method": "'+TvSortBy+'" } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	tvshows = jsonobject["result"]["tvshows"]	
	
	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["tvshowid", "episode", "originaltitle", "season", "streamdetails", "runtime"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	episodes = jsonobject["result"]["episodes"]
	
# create html output
def default_list():
	f = codecs.open(os.path.join(file_path,str(file_name)),'wt', "utf-8")
	# password_protect
	if (__addon__.getSetting('Enable_Password') == 'true'):
		f.write('<?php include("/data/www/'+__addon__.getSetting('webpage_location_php')+'/password_protect.php"); ?>\n')
	f.write('<!DOCTYPE html>\n')
	f.write('<head>\n')
	f.write('<meta  content="text/html;  charset=UTF-8"  http-equiv="Content-Type">\n')
	f.write('<title>'+__language__(30007)+' ('+time.strftime('%d %B %Y')+')</title>\n')
	f.write('<link rel="stylesheet" href="Default.css">\n')	
	f.write('<script language="JavaScript" charset="UTF-8" src="SearchScript.js"></script>\n')	
	f.write("</head>\n")
	f.write('<body background="http://images.wikia.com/monobook/images/7/7d/Binding_Dark.png">\n')
	f.write('<div id="header" style="height:95px;width:90%;position : fixed;background-color:#333333;margin-left: 5%;margin-right: auto ;">\n')
	f.write('<div id="Date" style="height:95px;width:20%;float:right;padding-right:1%;padding-top:15px;">\n')
	f.write('<p class="date">Last Updated: '+time.strftime('%d %B %Y')+'</p>\n')
	# password_protect logout
	if (__addon__.getSetting('Enable_Password') == 'true'):
		f.write('<form style="float:right;padding-top:30px;" method="get" action="password_protect.php" /><input type="submit" value="Logout" /><input type="hidden" name="logout" value="1" /></form>\n')
	f.write('</div>\n')
	f.write('<div id="Search" style="height:95px;width:20%;float:left;padding-left:1%;padding-top:15px;">\n')
	f.write("<iframe id="+'"srchform2" '+'src="'+"javascript:'<html><body style=margin:0px;><form action="+"\\'javascript:void();\\' onSubmit=if(this.t1.value!=\\'\\')parent.findString(this.t1.value);return(false);><input type=text id=t1 name=t1 size=20><input type=submit name=b1 value=Find></form></body></html>'"+'"'+" width=220 height=34 border=0 frameborder=0 scrolling=no></iframe>\n")
	if (__addon__.getSetting('includemovies') == 'true') and (__addon__.getSetting('includetvshows') == 'true'):
		f.write('<p class="links"><a href="#movie_link">Movies</a>&nbsp;&nbsp;<a href="#tvshow_link">TvShows</a></p>\n')
	f.write('</div>\n')
	f.write('<div id="Heading" style="height:95px;width:80%;margin-left: auto;margin-right: auto ;">\n')
	f.write('<h1><img src="http://xbmc.org/wp-content/themes/paradise/Paradise/images/logo.png" alt="XBMC" width="168" height="50" align="top"> '+__language__(30007)+'</h1>\n')
	f.write('</div>\n')
	f.write('</div>\n')
	f.write('<div id="Body" style="width:100%;padding-top:75px;">\n')

	if (__addon__.getSetting('includemovies') == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
		f.write('<a class="anchor" id="movie_link">anchor</a>\n')
		f.write('<hr width="90%">\n')
		f.write('<h2>MOVIES: ('+str(len(movies))+' Total / '+str(top250count)+ ' Top250)</h2>\n')
		f.write('<hr width="90%">\n')
		f.write('&nbsp;\n')
		for movie in movies:
			moviegenre = " / ".join(movie['genre'])
			movie_rating = '<span style="color:white"> &bull; </span><span style="color:gold">'+str(round(float(movie['rating']),1))+' &#9733;</span>'
			movie_runtime = '<span style="color:white"> &bull; '+str(movie['runtime'] / 60)+' min</span>' 
			if movie['streamdetails']['video'] != []:
				videowidth = movie['streamdetails']['video'][0]['width']
				videoheight = movie['streamdetails']['video'][0]['height']
				if videowidth <= 720 and videoheight <= 480:
					videoresolution = '<span style="color:white"> &bull; </span><span style="color:orange">480 SD</span>'
				elif videowidth <= 768 and videoheight <= 576:
					videoresolution = '<span style="color:white"> &bull; </span><span style="color:orange">576 SD</span>'
				elif videowidth <= 960 and videoheight <= 544:
					videoresolution = '<span style="color:white"> &bull; </span><span style="color:orange">540 SD</span>'
				elif videowidth <= 1280 and videoheight <= 720:
					videoresolution = '<span style="color:white"> &bull; </span><span style="color:deepskyblue">720 HD</span>'
				else:
					videoresolution = '<span style="color:white"> &bull; </span><span style="color:deepskyblue">1080 HD</span>'
			else:
				videoresolution = ''
			if movie['streamdetails']['audio'] != []:
				audiochannels = int(movie['streamdetails']['audio'][0]['channels'])
				if audiochannels == 8:
					channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">7.1 ch</span>'		
				elif audiochannels == 6:
					channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">5.1 ch</span>'
				elif audiochannels == 2:
					channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">2.0 ch</span>'
				elif audiochannels == 1:
					channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">1.0 ch</span>'
				else:
					channels = ''
			else:
				channels = ''			
			f.write('<p class="mediatitle">'+movie['label']+' ('+str(movie['year'])+')&nbsp;&nbsp;<a href="http://www.imdb.com/title/'+str(movie['imdbnumber'])+'/" target="_blank"><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/3/35/IMDb_logo.svg/200px-IMDb_logo.svg.png" alt="IMDB" width="30" height="14" align="bottom"></a></p>\n')	
			f.write('<p class="genre">'+str(moviegenre)+str(movie_rating))
			if int(movie['top250']) > 0:	
				f.write('<span style="color:gold"> ('+str(movie['top250'])+'/Top250)</span>'+str(movie_runtime)+str(videoresolution)+str(channels)+'</p>\n')
			else:
				f.write(str(movie_runtime)+str(videoresolution)+str(channels)+'</p>\n')		
			# format movie mpaa
			if str(movie['mpaa']).startswith("Rated"):
				f.write('<p class="mpaa">'+str(movie['mpaa'])+'</p>\n')
			elif str(movie['mpaa']) == "":
				f.write('<p class="mpaa">Rated NA</p>\n')
			else:
				f.write('<p class="mpaa">Rated '+str(movie['mpaa'])+'</p>\n')
			# list plot
			if (__addon__.getSetting('movieplot') == 'true'):
				f.write('<p class="plot">'+movie['plot']+'</p>\n')
				f.write('&nbsp;\n')
			else:
				f.write('&nbsp;\n')	
	
	if (__addon__.getSetting('includetvshows') == 'true') and xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
		f.write('<a class="anchor" id="tvshow_link">anchor</a>\n')
		f.write('<hr width="90%">\n')
		f.write('<h2>TV SHOWS: ('+str(len(tvshows))+' Total / '+str(len(episodes))+' Episodes)</h2>\n')
		if (__addon__.getSetting('episodes') == 'false'):
			f.write('<hr width="90%">\n')
		for tvshow in tvshows:
			tvgenre = " / ".join(tvshow['genre'])
			tv_rating = str(round(float(tvshow['rating']),1))
			if (__addon__.getSetting('episodes') == 'true'):
				f.write('<hr width="90%">\n')
			f.write('&nbsp;\n')
			f.write('<p class="mediatitle">' + tvshow['label']+' ('+str(tvshow['year'])+')&nbsp;&nbsp;<a href="http://thetvdb.com/?tab=series&amp;id=' + str(tvshow['imdbnumber']) + '/" target="_blank"><img src="http://home.comcast.net/~krkweb/xbmc/thetvdb_logo_onblack.jpg" alt="TVDB" width="30" height="14" align="bottom"></a></p>\n')			
			episode_list = []
			for episode in episodes:
				episode_runtime = ' &bull; '+str(episode['runtime'] / 60)+' min'
				if (__addon__.getSetting('episodes') == 'true'):					
					if episode['streamdetails']['video'] != []:
						videowidth = episode['streamdetails']['video'][0]['width']
						videoheight = episode['streamdetails']['video'][0]['height']
						if videowidth <= 720 and videoheight <= 480:
							videoresolution = ' &bull; <span style="color:orange">480 SD</span>'
						elif videowidth <= 768 and videoheight <= 576:
							videoresolution = ' &bull; <span style="color:orange">576 SD</span>'
						elif videowidth <= 960 and videoheight <= 544:
							videoresolution = ' &bull; <span style="color:orange">540 SD</span>'
						elif videowidth <= 1280 and videoheight <= 720:
							videoresolution = ' &bull; <span style="color:deepskyblue">720 HD</span>'
						else:
							videoresolution = ' &bull; <span style="color:deepskyblue">1080 HD</span>'
					else:
						videoresolution = ''				
					if episode['streamdetails']['audio'] != []:
						audiochannels = int(episode['streamdetails']['audio'][0]['channels'])
						if audiochannels == 8:
							channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">7.1 ch</span>'		
						elif audiochannels == 6:
							channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">5.1 ch</span>'
						elif audiochannels == 2:
							channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">2.0 ch</span>'
						elif audiochannels == 1:
							channels = '<span style="color:white"> &bull; </span><span style="color:darkgrey">1.0 ch</span>'
						else:
							channels = ''
					else:
						channels = ''				
				if episode['tvshowid'] == tvshow['tvshowid']:
					episode_list.append((episode['season'],episode['episode'],episode['label']+str(episode_runtime)+str(videoresolution)+str(channels)))
			episode_list.sort()
			if (__addon__.getSetting('episodes') == 'false'):
				prev_season = None
				seasoncount = 0
				for episode in episode_list:
					season = episode[0]		
					if season != prev_season:
						seasoncount += 1			
						prev_season = season
				f.write('<p class="episodecount">(Seasons ' +str(seasoncount)+' / '+str(len(episode_list))+' Episodes)</p>\n')		
			f.write('<p class="genre">'+str(tvgenre)+' <span style="color:white">&bull;</span> <span style="color:gold"> '+str(tv_rating)+' &#9733;</span></p>\n')
			# format tvshow mpaa
			if str(tvshow['mpaa']) == "":
				f.write('<p class="mpaa">Rated NA</p>\n')
			else:
				f.write('<p class="mpaa">Rated '+str(tvshow['mpaa'])+'</p>\n')
			# list plot
			if (__addon__.getSetting('tvshowplot') == 'true'):
				f.write('<p class="plot">'+tvshow['plot']+'</p>\n')	
			# list episodes
			if (__addon__.getSetting('episodes') == 'true'):
				prev_season = None
				for episode in episode_list:
					season = episode[0]			
					if season != prev_season:						
						f.write('<h3>Season '+str(season)+'</h3>\n')
						prev_season = season
					f.write('<p class="episode">'+episode[2]+'</p>\n')
				f.write('&nbsp;\n')
		if (__addon__.getSetting('episodes') == 'false'):
			f.write('&nbsp;\n')
	f.write('</div>\n')
	f.write('<div id="footer">\n')
	f.write('<hr width="90%">\n')
	f.write('<div style="float:right;padding-right:5.5%;padding-bottom:10px;">\n')
	f.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;">Created using: <a href="https://github.com/Steveb1968/script.html.library-report" target="_blank">script.html.library-report</a> by Steveb</p>\n')
	f.write('<p style="font-size:0.8em;color:white;text-shadow:1px 1px black;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;float:right;">Help/Support: <a href="http://forum.xbmc.org/showthread.php?tid=167632" target="_blank">script.html.library-report</a></p>\n')
	f.write('</div>\n')
	f.write('</div>\n')
	f.write('</body>\n')
	f.write('</html>')
	f.close()
	
if (__addon__.getSetting('Enable_ftp') == 'false'):
	xbmc.executebuiltin( "Dialog.Close(busydialog)" )
	xbmc.sleep(200)
	xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addon__.getAddonInfo('name'), __language__(30005), 4000, __icon__) )
else:
	xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ( __language__(30005), __language__(30006), 4000, __icon__) )
	
def copy_files():	
	web_files = os.listdir(__files__)
	for file_name in web_files:
		full_file_name = os.path.join(__files__, file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, file_path)

def password_protect():
	password_php = xbmc.translatePath( os.path.join( __resource__, 'php', 'password_protect.php' ).encode("utf-8") ).decode("utf-8")		
	with codecs.open(password_php, "r", encoding="utf-8") as file:
		data = file.readlines()
	# change the selected lines
	data[51] = "\t'"+__addon__.getSetting('web_user')+"' => '"+__addon__.getSetting('web_password')+"'\n"
	data[58] = "define('LOGOUT_URL', 'http://"+__addon__.getSetting('logout_url')+"/');\n"
	# write back
	with codecs.open(password_php, "w", encoding="utf-8") as file:
		file.writelines(data)
		file.close()
	
# ftp file transfer
def ftp():

	def chdir(session, directory):
		ch_dir_rec(session,directory.split('/'))

	# Check if directory exists (in current location)
	def directory_exists(session, directory):
		filelist = []
		session.retrlines('LIST',filelist.append)
		for f in filelist:
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

	try:
		session = ftplib.FTP(__addon__.getSetting('server'),__addon__.getSetting('user'),__addon__.getSetting('password'))
		if (__addon__.getSetting('enable_ftp_dir') == 'true') and directory != "":
			chdir(session, directory)
		if (__addon__.getSetting('Enable_Password') == 'true'):
			filepass = open( os.path.join( __resource__, 'php', 'password_protect.php' ),'rb')			
			session.storlines('STOR ' + str(password_file), filepass)
			filepass.close()
		file = open(str(file_path)+str(file_name),'rb')	
		session.storlines('STOR ' + str(file_name), file)
		file.close()		
		file = open( os.path.join( __resource__, 'files', 'Default.css' ),'rb')	
		session.storlines('STOR ' + 'Default.css', file)		
		file.close()		
		file = open( os.path.join( __resource__, 'files', 'SearchScript.js' ),'rb')	
		session.storlines('STOR ' + 'SearchScript.js', file)		
		file.close()		
		session.quit()		
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
		xbmc.sleep(200)
		xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__addon__.getAddonInfo('name'),__language__(30025), 4000, __icon__) )
	except Exception,e:
		xbmc.executebuiltin( "Dialog.Close(busydialog)" )
		xbmc.sleep(200)
		xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (__language__(30026),e, 4000, __icon__) )

if ( __name__ == "__main__" ):
	xbmc.log(__addon__.getAddonInfo('name')+": ## STARTED")
	default_list()
	copy_files()
	if (__addon__.getSetting('Enable_Password') == 'true'):
		password_protect()
	if (__addon__.getSetting('Enable_ftp') == 'true'):
		xbmc.log(__addon__.getAddonInfo('name')+": ## UPLOADING TO FTP HOST")
		ftp()
	xbmc.log(__addon__.getAddonInfo('name')+": ## FINISHED")
	sys.modules.clear()