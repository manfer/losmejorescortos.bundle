# -*- coding: utf-8 -*-
TITLE  = u'Los Mejores Cortos'
PREFIX = '/video/losmejorescortos'

LMC_BASE_URL = 'http://www.losmejorescortos.com'
LMC_ALL = LMC_BASE_URL + "/todos"
LMC_TAGS = LMC_BASE_URL + "/nube-de-etiquetas"
LMC_TAG = LMC_BASE_URL + "/tag/{0}/"
LMC_CATEGORY = LMC_BASE_URL + "/category/cortos/{0}/"
LMC_SHORT = LMC_BASE_URL + "/{0}"
LMC_SEARCH = LMC_BASE_URL + "/?s={0}"
LMC_SEARCH_PAGE = LMC_BASE_URL + "/page/{0}/?s={1}"

LMC_URL_PATTERN = Regex('.*?losmejorescortos.com/(.*)/')
LMC_CATEGORY_PATTERN = Regex('.*?losmejorescortos.com/category/cortos/(.*)/')
LMC_TAG_PATTERN = Regex('.*?losmejorescortos.com/tag/(.*)/')

LMC_ICON      = 'losmejorescortos.png'
ICON          = 'default-icon.png'
ART           = 'homecinema.jpg'
SEARCH_ICON   = 'search-icon.png'
NEXT_ICON     = 'next-icon.png'
SETTINGS_ICON = 'settings-icon.png'

HTTP_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Connection': 'keep-alive',
  'Referer': 'http://www.losmejorescortos.com/'
}

################################################################################
def Start():

  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = TITLE
  #ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)

  Locale.DefaultLocale = Prefs["language"].split("/")[1]

  HTTP.CacheTime = CACHE_1HOUR

################################################################################
@handler(PREFIX, TITLE, art=ART, thumb=LMC_ICON)
def lmc_main_menu():

  oc = ObjectContainer()

  oc.add(DirectoryObject(
    key     = Callback(lmc_get_just_added),
    title   = L('Just Added'),
    summary = L('just added shorts')
  ))

  oc.add(DirectoryObject(
    key     = Callback(lmc_get_all, page = 1),
    title   = L('All'),
    summary = L('shorts full list')
  ))

  oc.add(DirectoryObject(
    key     = Callback(lmc_get_categories),
    title   = L('Categories'),
    summary = L('choose the category you want to view')
  ))

  oc.add(DirectoryObject(
    key     = Callback(lmc_get_tags),
    title   = L('Tags'),
    summary = L('choose a tag from our tags of cloud')
  ))

  oc.add(DirectoryObject(
    key     = Callback(lmc_favorites),
    title   = L('Favorites'),
    summary = L('play one of your favorite shorts')
  ))

  oc.add(PrefsObject(
    title = L('Preferences'),
    thumb = R(SETTINGS_ICON)
  ))

  if Client.Product != 'PlexConnect':
    oc.add(InputDirectoryObject(
      key     = Callback(lmc_search),
      title   = L('Search Shorts'),
      prompt  = L('Search for Shorts'),
      summary = L('Search for Shorts'),
      thumb   = R(SEARCH_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/justadded')
def lmc_get_just_added():

  oc = ObjectContainer(
    title2 = L('Just Added')
  )

  for short in HTML.ElementFromURL(LMC_BASE_URL, headers=HTTP_HEADERS).xpath('//div[@class="nag cf"]/div'):
    short_title   = short.xpath('.//h2[@class="title"]/a/text()')[0]
    short_url     = short.xpath('.//h2[@class="title"]/a/@href')[0]
    short_thumb   = short.xpath('.//div[@class="thumb"]//img/@src')[0]
    short_summary = short.xpath('.//p[@class="desc"]/text()')[0]
    short_url     = LMC_URL_PATTERN.search(short_url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_short, short = short_url, thumb = short_thumb),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(short_thumb)
    ))

  return oc

################################################################################
@route(PREFIX+'/all', page=int)
def lmc_get_all(page = 1):

  page = int(page)

  oc = ObjectContainer(
    title2 = unicode(L('All') + ' | ' + L('Page') + ' ' + str(page))
  )

  url = LMC_ALL if (page == 1) else LMC_ALL + '/page/' + str(page)
  content = HTML.ElementFromURL(url, headers = HTTP_HEADERS)

  for short in content.xpath('//div[@class="nag cf"]/div'):
    short_title   = short.xpath('.//h2[@class="title"]/a/text()')[0]
    short_url     = short.xpath('.//h2[@class="title"]/a/@href')[0]
    short_thumb   = short.xpath('.//div[@class="thumb"]//img/@src')[0]
    short_summary = short.xpath('.//p[@class="desc"]/text()')[0]
    short_url     = LMC_URL_PATTERN.search(short_url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_short, short = short_url, thumb = short_thumb),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(short_thumb)
    ))

  paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

  if len(paginador) > 0:
    oc.add(NextPageObject(
      key   = Callback(lmc_get_all, page = page + 1),
      title = L('Next Page') + ' >>',
      thumb = R(NEXT_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/categories')
def lmc_get_categories():

  oc = ObjectContainer(
    title2 = L('Categories')
  )

  for category in HTML.ElementFromURL(LMC_BASE_URL, headers=HTTP_HEADERS).xpath('//li[@id="menu-item-52"]/ul/li/a'):
    url      = category.get('href')
    title    = category.text
    catname  = 'trailers' if ('trailers' in url) else LMC_CATEGORY_PATTERN.search(url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_category, title = title, category = catname, page = 1),
      title   = title
    ))

  return oc

################################################################################
@route(PREFIX+'/category/{category}', page=int)
def lmc_get_category(title, category, page = 1):

  page = int(page) 

  oc = ObjectContainer(
    title2 = unicode(L('Category') + ': ' + title  + ' | ' + L('Page') + ' ' + str(page))
  )

  url = LMC_CATEGORY.format(category) if (page == 1) else LMC_CATEGORY.format(category + '/page/' + str(page))
  content = HTML.ElementFromURL(url, headers = HTTP_HEADERS)

  for short in content.xpath('//div[@class="nag cf"]/div'):
    short_title   = short.xpath('.//h2[@class="title"]/a/text()')[0]
    short_url     = short.xpath('.//h2[@class="title"]/a/@href')[0]
    short_thumb   = short.xpath('.//div[@class="thumb"]//img/@src')[0]
    short_summary = short.xpath('.//p[@class="desc"]/text()')[0]
    short_url     = LMC_URL_PATTERN.search(short_url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_short, short = short_url, thumb = short_thumb),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(short_thumb)
    ))

  paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

  if len(paginador) > 0:
    oc.add(NextPageObject(
      key = Callback(lmc_get_category, title = title, category = category, page = page + 1),
      title = L('Next Page') + ' >>',
      thumb = R(NEXT_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/tags')
def lmc_get_tags():

  oc = ObjectContainer(
    title2 = L('Tags')
  )

  for tag in HTML.ElementFromURL(LMC_TAGS, headers=HTTP_HEADERS).xpath('//div[@class="term-cloud post_tag-cloud tag-cloud"]/a'):
    url     = tag.get('href')
    title   = tag.text
    Log.Info(title)
    tagname = LMC_TAG_PATTERN.search(url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_tag, title = title, tag = tagname, page = 1),
      title   = title
    ))

  return oc

################################################################################
@route(PREFIX+'/tag/{tag}', page=int)
def lmc_get_tag(title, tag, page = 1):

  page = int(page)

  oc = ObjectContainer(
    title2 = unicode(L('Tag') + ': ' + title + ' | ' + L('Page') + ' ' + str(page))
  )

  url = LMC_TAG.format(tag) if (page == 1) else LMC_TAG.format(tag + '/page/' + str(page))
  content = HTML.ElementFromURL(url, headers=HTTP_HEADERS)

  for short in content.xpath('//div[@class="nag cf"]/div'):
    short_title   = short.xpath('.//h2[@class="title"]/a/text()')[0]
    short_url     = short.xpath('.//h2[@class="title"]/a/@href')[0]
    short_thumb   = short.xpath('.//div[@class="thumb"]//img/@src')[0]
    short_summary = short.xpath('.//p[@class="desc"]/text()')[0]
    short_url     = LMC_URL_PATTERN.search(short_url).group(1)

    oc.add(DirectoryObject(
      key     = Callback(lmc_get_short, short = short_url, thumb = short_thumb),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(short_thumb)
    ))

  paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

  if len(paginador) > 0:
    oc.add(NextPageObject(
      key = Callback(lmc_get_tag, title = title, tag = tag, page = page + 1),
      title = L('Next Page') + ' >>',
      thumb = R(NEXT_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/short/{short}')
def lmc_get_short(short, thumb):

  url = LMC_SHORT.format(short)

  content = HTML.ElementFromURL(url, headers=HTTP_HEADERS)

  title   = content.xpath('//h1[@id="title"]/text()')[0]
  video   = content.xpath('//div[@id="video"]//iframe/@src')[0]

  oc = ObjectContainer(
    title2 = title
  )

  oc.add(URLService.MetadataObjectForURL(video))

  if Data.Exists('LMCFavorites'):
    favorites = Data.LoadObject('LMCFavorites')
    if short in favorites:
      oc.add(DirectoryObject(
        key = Callback(RemovefromFavorites, short = short),
        title = L('Remove from Favorites')
      ))
    else:
      oc.add(DirectoryObject(
        key = Callback(AddtoFavorites, short = short, title = title, thumb = thumb),
        title = L('Add to Favorites')
      ))
  else:
    oc.add(DirectoryObject(
      key = Callback(AddtoFavorites, short = short, title = title, thumb = thumb),
      title = L('Add to Favorites')
    ))

  return oc

def L(string):
  local_string = Locale.LocalString(string)
  return str(local_string).decode()

from LMCFavorites import *
from LMCSearch import *
