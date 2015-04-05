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

from LMCUtil import L
from LMCShorts import *
from LMCFavorites import *
from LMCSearch import *

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
