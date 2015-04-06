# -*- coding: utf-8 -*-
from LMCUtil import L
from LMCFavorites import AddtoFavorites, RemovefromFavorites

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
      key = Callback(
        lmc_get_short,
        short = short_url,
        thumb = short_thumb,
        title = short_title
      ),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(url = short_thumb),
      art     = Resource.ContentsOfURLWithFallback(url = short_thumb)
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
      key = Callback(
        lmc_get_short,
        short = short_url,
        thumb = short_thumb,
        title = short_title
      ),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(url = short_thumb),
      art     = Resource.ContentsOfURLWithFallback(url = short_thumb)
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
      key = Callback(
        lmc_get_category,
        title = title,
        category = catname,
        page = 1
      ),
      title = title
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
      key = Callback(
        lmc_get_short,
        short = short_url,
        thumb = short_thumb,
        title = short_title
      ),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(url = short_thumb),
      art     = Resource.ContentsOfURLWithFallback(url = short_thumb)
    ))

  paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

  if len(paginador) > 0:
    oc.add(NextPageObject(
      key = Callback(
        lmc_get_category,
        title = title,
        category = category,
        page = page + 1
      ),
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
      key = Callback(
        lmc_get_tag,
        title = title,
        tag = tagname,
        page = 1
      ),
      title = title
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
      key = Callback(
        lmc_get_short,
        short = short_url,
        thumb = short_thumb,
        title = short_title
      ),
      title   = short_title,
      summary = short_summary,
      thumb   = Resource.ContentsOfURLWithFallback(url = short_thumb),
      art     = Resource.ContentsOfURLWithFallback(url = short_thumb)
    ))

  paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

  if len(paginador) > 0:
    oc.add(NextPageObject(
      key = Callback(
        lmc_get_tag,
        title = title,
        tag = tag,
        page = page + 1
      ),
      title = L('Next Page') + ' >>',
      thumb = R(NEXT_ICON)
    ))

  return oc

################################################################################
@route(PREFIX+'/short/{short}')
def lmc_get_short(short, thumb, title):

  url = LMC_SHORT.format(short)

  oc = ObjectContainer(
    title2 = unicode(title)
  )

  oc.add(VideoClipObject(
    url = url,
    title = title,
    thumb = Resource.ContentsOfURLWithFallback(url = thumb),
    art = Resource.ContentsOfURLWithFallback(url = thumb)
  ))

  if Data.Exists('LMCFavorites'):
    favorites = Data.LoadObject('LMCFavorites')
    if short in favorites:
      oc.add(DirectoryObject(
        key = Callback(
          RemovefromFavorites,
          short = short
        ),
        title = L('Remove from Favorites')
      ))
    else:
      oc.add(DirectoryObject(
        key = Callback(
          AddtoFavorites,
          short = short,
          title = title,
          thumb = thumb
        ),
        title = L('Add to Favorites')
      ))
  else:
    oc.add(DirectoryObject(
      key = Callback(
        AddtoFavorites,
        short = short,
        title = title,
        thumb = thumb
      ),
      title = L('Add to Favorites')
    ))

  return oc
