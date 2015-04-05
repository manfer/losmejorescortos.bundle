# -*- coding: utf-8 -*-
@route(PREFIX+'/add')
def AddtoFavorites(short, title, thumb):
  metadata = {
    'short': short,
    'title': unicode(title),
    'thumb': thumb
  }
  try:
    favs = {}
    if Data.Exists('LMCFavorites'):
      favs = Data.LoadObject('LMCFavorites')
    if short not in favs:
      favs[short] = metadata
      Data.SaveObject('LMCFavorites', favs)
    return ObjectContainer(
      header   = L('Added to Favorites'),
      message  = L('The short had been added to your Favorites'),
      no_cache = True
    )
  except:
    Log.Debug(L('Error when trying to add short to Favorites'))

@route(PREFIX+'/remove')
def RemovefromFavorites(short):
  try:
    favs = Data.LoadObject('LMCFavorites')
    if short in favs:
      del favs[short]
      Data.SaveObject('LMCFavorites', favs)
      return ObjectContainer(
        header   = L('Removed from Favorites'),
        message  = L('The Short had been removed from your Favorites'),
        no_cache = True
      )
  except:
    Log.Debug(L('Error when trying to remove short from Favorites'))

@route(PREFIX+'/favorites')
def lmc_favorites():
  nofav = ObjectContainer(
    header   = L('No Favorites'),
    message  = L('You have to add at least a short to your Favorites'),
    no_cache = True
  )
  if Data.Exists('LMCFavorites'):
    try:
      favs = Data.LoadObject('LMCFavorites')
      values = favs.values()
      if not values:
        return nofav
      else:
        oc = ObjectContainer(
          title2 = L('Favorites')
        )
        for short in values:
          Log.Info(short)
          oc.add(DirectoryObject(
            key   = Callback(lmc_get_short, short = short["short"], thumb = short["thumb"]),
            title = short["title"],
            thumb = Resource.ContentsOfURLWithFallback(url = short["thumb"]),
            art   = Resource.ContentsOfURLWithFallback(url = short["thumb"])
          ))
        return oc
    except:
      return nofav
  else:
    return nofav
