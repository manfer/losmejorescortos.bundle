# -*- coding: utf-8 -*-
@route(PREFIX+'/search', page = int)
def lmc_search(query, page = 1):

  oc = ObjectContainer(
    title2 = unicode(L('Search Results') + ': ' + query  + ' | ' + L('Page') + ' ' + str(page))
  )

  noresults = ObjectContainer(
    header   = L('Short not found'),
    message  = L('Short not found'),
    no_cache = True
  )

  url = LMC_SEARCH.format(query) if (page == 1) else LMC_SEARCH_PAGE.format(str(page), query) 
  content = HTML.ElementFromURL(url, headers = HTTP_HEADERS)
  shorts  = content.xpath('//div[@class="nag cf"]/div')

  if len(shorts) > 0:
    for short in shorts:
      short_title   = short.xpath('.//h2[@class="title"]/a/text()')[0]
      short_url     = short.xpath('.//h2[@class="title"]/a/@href')[0]
      short_thumb   = short.xpath('.//div[@class="thumb"]//img/@src')[0]
      short_summary = short.xpath('.//p[@class="desc"]/text()')[0]
      short_url     = LMC_URL_PATTERN.search(short_url).group(1)

      oc.add(DirectoryObject(
        key     = Callback(lmc_get_short, short = short_url, thumb = short_thumb),
        title   = short_title,
        summary = short_summary,
        thumb   = Resource.ContentsOfURLWithFallback(url = short_thumb),
        art     = Resource.ContentsOfURLWithFallback(url = short_thumb)
      ))

    paginador = content.xpath('//div[@class="wp-pagenavi"]/span[@class="current"]/following-sibling::a')

    if len(paginador) > 0:
      oc.add(NextPageObject(
        key = Callback(lmc_search, query = query, page = page + 1),
        title = L('Next Page') + ' >>',
        thumb = R(NEXT_ICON)
      ))

    return oc
  else:
    return noresults
