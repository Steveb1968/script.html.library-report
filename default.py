import os
import xbmc
import xbmcgui
import xbmcaddon
import time
import codecs
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__ = xbmcaddon.Addon(id='script.html.library-report')
__language__  = __addon__.getLocalizedString

#save path
file_path = __addon__.getSetting('save_location')
while file_path=="":
	xbmcgui.Dialog().ok(__addon__.getAddonInfo('name'),__language__(30004))
	__addon__.openSettings()
	file_path = __addon__.getSetting('save_location')

#data
if xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties" : ["genre", "plotoutline", "plot", "rating", "year", "runtime", "mpaa", "imdbnumber", "top250"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	movies = jsonobject["result"]["movies"]

if xbmc.getCondVisibility( "Library.HasContent(TVShows)" ):
	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["genre", "title", "plot", "rating", "originaltitle", "year", "mpaa", "imdbnumber"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	tvshows = jsonobject["result"]["tvshows"]

	command='{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"properties": ["tvshowid", "episode", "originaltitle", "season"], "sort": { "order": "ascending", "method": "label" } }, "id": 1}'
	result = xbmc.executeJSONRPC( command )
	result = unicode(result, 'utf-8', errors='ignore')
	jsonobject = simplejson.loads(result)
	episodes = jsonobject["result"]["episodes"]
	
file_name = "XBMC "+__language__(30007)

#create html output
f = codecs.open(os.path.join(file_path,str(file_name)+'.html'),'wt', "utf-8")
f.write('<!DOCTYPE html>\n')
f.write('<head>\n')
f.write('<meta  content="text/html;  charset=UTF-8"  http-equiv="Content-Type">\n')
f.write('<title>XBMC '+__language__(30007)+' ('+time.strftime('%d %B %Y')+')</title>\n')
f.write('<style type="text/css">\n')
f.write("body {background-image:url('http://subtlepatterns.com/patterns/binding_dark.png');background-color:#000000;}\n")
f.write('h1 {font-weight:bold;color:gold;text-shadow:1px 1px black;text-align:center;font-family:Verdana, Geneva, sans-serif;}\n')
f.write('h2 {font-weight:bold;color:white;text-shadow:1px 1px black;text-align:center;font-family:"Trebuchet MS", Helvetica, sans-serif;}\n')
f.write('h3 {font-weight:bold;color:cyan;text-shadow:1px 1px black;text-align:center;text-decoration:underline;font-family:Arial, Helvetica, sans-serif;}\n')
f.write('p.mediatitle {font-size:1.35em;font-weight:bold;color:white;text-shadow:1px 1px black;text-align:center;font-family:"Times New Roman", Times, serif;margin:0;line-height:1.0;}\n')
f.write('p.episode {font-size:1.0em;color:white;text-align:center;font-family:"Courier New", Courier, monospace;margin:0;line-height:1.2;}\n')
f.write('p.plot {font-size:1.0em;color:white;text-align:center;font-family:"Courier New", Courier, monospace;padding:0% 5% 0% 5%;}\n')
f.write('p.episodecount {font-size:0.9em;color:cyan;text-shadow:1px 1px black;text-align:center;font-family:Arial, Helvetica, sans-serif;margin:5px;line-height:1.2;}\n')
f.write('p.genre {font-size:1.0em;color:yellowgreen;text-shadow:1px 1px black;text-align:center;font-family:Arial, Helvetica, sans-serif;margin:6px;line-height:1.2;}\n')
f.write('p.mpaa {font-size:0.8em;color:white;text-shadow:1px 1px black;text-align:center;font-family:Arial, Helvetica, sans-serif;margin:6px;line-height:1.2;}\n')
f.write('p.date {font-size:0.9em;color:white;text-shadow:1px 1px black;text-align:right;font-family:Arial, Helvetica, sans-serif;margin:0;line-height:1.2;}\n')
f.write('p.links {color:white;text-shadow:1px 1px black;margin: 0 ;padding-top:10px;font-family:Arial, Helvetica, sans-serif;}\n')
f.write('a.anchor{display: block; position: relative; top: -90px; visibility: hidden;}\n')
f.write('</style>\n')
f.write('<script language="JavaScript">\n')
f.write('var TRange=null;\n')
f.write('function findString (str) {\n')
f.write('\tif (parseInt(navigator.appVersion)<4) return;\n')
f.write('\tvar strFound;\n')
f.write('\tif (window.find) {\n')
f.write('\t\tstrFound=self.find(str);\n')
f.write('\t\tif (!strFound) {\n')
f.write('\t\t\tstrFound=self.find(str,0,1);\n')
f.write('\t\t\twhile (self.find(str,0,1)) continue;\n')
f.write('\t\t}\n')
f.write('\t}\n')
f.write('\t	else if (navigator.appName.indexOf("Microsoft")!=-1) {\n')
f.write('\t\tif (TRange!=null) {\n')
f.write('\t\t\tTRange.collapse(false);\n')
f.write('\t\t\tstrFound=TRange.findText(str);\n')
f.write('\t\t\tif (strFound) TRange.select();\n')
f.write('\t\t}\n')
f.write('\t\tif (TRange==null || strFound==0) {\n')
f.write('\t\t\tTRange=self.document.body.createTextRange();\n')
f.write('\t\t\tstrFound=TRange.findText(str);\n')
f.write('\t\t\tif (strFound) TRange.select();\n')
f.write('\t\t}\n')
f.write('\t}\n')
f.write('\telse if (navigator.appName=="Opera") {\n')
f.write('\t\talert ("Opera browsers not supported, sorry...")\n')
f.write('\t\treturn;\n')
f.write('\t}\n')
f.write('\tif (!strFound) alert ("String ''"+str+"'' not found!")\n')
f.write('\treturn;\n')
f.write('}\n')
f.write('</script>\n')
f.write("</head>\n")
f.write('<body style="margin: 0;padding: 0; link="white" vlink="white" alink="red">\n')
f.write('<div id="Header" style="height:95px;width:90%;position : fixed;background-color:#333333;margin-left: 5%;margin-right: auto ;">\n')
f.write('<div id="Date" style="height:30px;width:20%;float:right;padding-right:1%;padding-top:15px;">\n')
f.write('<p class="date">Last Updated: '+time.strftime('%d %B %Y')+'</p>\n')
f.write('</div>\n')
f.write('<div id="Search" style="height:30px;width:20%;float:left;padding-left:1%;padding-top:15px;">\n')
f.write("<iframe id="+'"srchform2" '+'src="'+"javascript:'<html><body style=margin:0px;><form action="+"\\'javascript:void();\\' onSubmit=if(this.t1.value!=\\'\\')parent.findString(this.t1.value);return(false);><input type=text id=t1 name=t1 size=20><input type=submit name=b1 value=Find></form></body></html>'"+'"'+" width=220 height=34 border=0 frameborder=0 scrolling=no></iframe>\n")
if (__addon__.getSetting('includemovies') == 'true') and (__addon__.getSetting('includetvshows') == 'true'):
	f.write('<p class="links"><a href="#movie_link">Movies</a>&nbsp;&nbsp;<a href="#tvshow_link">TvShows</a></p>\n')
f.write('</div>\n')
f.write('<div id="Heading" style="height:65px;width:80%;margin-left: auto;margin-right: auto ;">\n')
f.write('<h1><img src="http://wiki.xbmc.org/images/thumb/9/9b/XBMC_logo-solid_shadow.png/800px-XBMC_logo-solid_shadow.png" alt="XBMC" width="93" height="50" align="top"> '+__language__(30007)+'</h1>\n')
f.write('</div>\n')
f.write('</div>\n')
f.write('<div id="Body" style="width:100%;padding-top:90px;">\n')

if (__addon__.getSetting('includemovies') == 'true') and xbmc.getCondVisibility( "Library.HasContent(Movies)" ):
	f.write('<a class="anchor" id="movie_link">anchor</a>\n')
	f.write('<hr width="90%">\n')
	top250count = 0
	for movie in movies:
		if int(movie['top250']) > 0:
			top250count += 1
	f.write('<h2>MOVIES: ('+str(len(movies))+' Total / '+str(top250count)+ ' Top250)</h2>\n')
	f.write('<hr width="90%">\n')
	f.write('&nbsp;\n')
	for movie in movies:
		f.write('<p class="mediatitle">'+movie['label']+' ('+str(movie['year'])+')&nbsp;&nbsp;<a href="http://www.imdb.com/title/'+str(movie['imdbnumber'])+'/" target="_blank"><img src="http://upload.wikimedia.org/wikipedia/commons/3/35/IMDb_logo.svg" alt="IMDB" width="30" height="14" align="bottom"></a></p>\n')					
		#format movie genre	
		moviegenre = str(movie['genre'])
		moviegenre = moviegenre.replace("u'",'')
		b = "[]'"
		c = ","
		for i in range(0,len(b)):
			moviegenre = moviegenre.replace(b[i],"")
			for i in range(0,len(c)):
				moviegenre = moviegenre.replace(c[i]," /")
		#format movie rating	
		movie_rating = float(str(movie['rating']))
		movie_rating = "%.1f" % movie_rating	
		f.write('<p class="genre">'+str(moviegenre)+' <span style="color:white">&bull;</span> <span style="color:gold"> '+str(movie_rating))
		if int(movie['top250']) > 0:	
			f.write(' &#9733; '+'('+str(movie['top250'])+'/Top250)</span></p>\n')
		else:
			f.write(' &#9733;</span></p>\n')		
		#format movie mpaa
		if str(movie['mpaa']).startswith("Rated"):
			f.write('<p class="mpaa">'+str(movie['mpaa'])+'</p>\n')
		elif str(movie['mpaa']) == "":
			f.write('<p class="mpaa">Rated NA</p>\n')
		else:
			f.write('<p class="mpaa">Rated '+str(movie['mpaa'])+'</p>\n')
		#list plot
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
		if (__addon__.getSetting('episodes') == 'true'):
			f.write('<hr width="90%">\n')
		f.write('&nbsp;\n')
		f.write('<p class="mediatitle">' + tvshow['label']+' ('+str(tvshow['year'])+')&nbsp;&nbsp;<a href="http://thetvdb.com/?tab=series&id=' + str(tvshow['imdbnumber']) + '/" target="_blank"><img src="http://home.comcast.net/~krkweb/xbmc/thetvdb_logo_onblack.jpg" alt="TVDB" width="30" height="14" align="bottom"></a></p>\n')			
		episode_list = []
		for episode in episodes:
			if episode['tvshowid'] == tvshow['tvshowid']:
				episode_list.append((episode['season'],episode['episode'],episode['label']))	
		episode_list.sort()	
		prev_season = None
		seasoncount = 0
		for episode in episode_list:
			season = episode[0]		
			if season != prev_season:
				seasoncount += 1			
				prev_season = season
		f.write('<p class="episodecount">(Seasons ' +str(seasoncount)+' / '+str(len(episode_list))+' Episodes)</p>\n')	
		#format tvshow genre	
		tvgenre = str(tvshow['genre'])
		tvgenre = tvgenre.replace("u'",'')
		d = "[]'"
		e = ","
		for i in range(0,len(d)):
			tvgenre = tvgenre.replace(d[i],"")
			for i in range(0,len(e)):
				tvgenre = tvgenre.replace(e[i]," /")	
		#format tvshow rating		
		tv_rating = float(str(tvshow['rating']))
		tv_rating = "%.1f" % tv_rating	
		f.write('<p class="genre">'+str(tvgenre)+' <span style="color:white">&bull;</span> <span style="color:gold"> '+str(tv_rating)+' &#9733;</span></p>\n')
		#format tvshow mpaa
		if str(tvshow['mpaa']) == "":
			f.write('<p class="mpaa">Rated NA</p>\n')
		else:
			f.write('<p class="mpaa">Rated '+str(tvshow['mpaa'])+'</p>\n')
		#list plot
		if (__addon__.getSetting('tvshowplot') == 'true'):
			f.write('<p class="plot">'+tvshow['plot']+'</p>\n')	
		#list episodes
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
f.write('</body>\n')
f.write('</html>')
f.close()

xbmcgui.Dialog().ok(__addon__.getAddonInfo('name'),__language__(30005),__language__(30006),str(file_path)+str(file_name)+".html")
