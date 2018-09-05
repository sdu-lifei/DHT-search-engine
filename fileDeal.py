# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:38:58 2015
@author: aneasystone
"""

import libtorrent as lt
import time

max_times = 10

'''
    transfer a torrent file to a magnet link
'''


def torrent2magnet(torrent_file):
    info = lt.torrent_info(torrent_file)
    print "info is:",info.files()
    link = "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
    print link
    return link


'''
    transfer a magnet link to a torrent file
'''

dhtSess = lt.session()
params = {
        "save_path": './newfiles/',
        "storage_mode":lt.storage_mode_t.storage_mode_sparse,
        "paused": True,
        "auto_managed": True,
        "duplicate_is_error": True
    }

def magnet2torrent(link):

    print "link is: %s" % link

    dhtSess.add_dht_router('router.bittorrent.com', 6881)
    dhtSess.add_dht_router('router.utorrent.com', 6881)
    dhtSess.add_dht_router('router.bitcomet.com', 6881)
    dhtSess.add_dht_router('dht.transmissionbt.com', 6881)
    dhtSess.start_dht();

    handle = lt.add_magnet_uri(dhtSess, link, params)

    # waiting for metadata
    tt = 1
    while (not handle.has_metadata()):
        time.sleep(1)
        if (tt >= max_times):
            print "no proper res!!!"
            return 2
        tt += 1

    # create a torrent
    torinfo = handle.get_torrent_info()

    # print info
    print 'got %s' % torinfo.name()

    torrent_file = link

    if torinfo.name():
        torrent_file = torinfo.name()


    torfile = lt.create_torrent(torinfo)
    torcontent = lt.bencode(torfile.generate())

    # save to file
    t = open(torrent_file + ".torrent", "wb")
    t.write(torcontent)
    t.close()

    return 0

def findFiles(ihfile):

    for info in ihfile:
        info = "magnet:?xt=urn:btih:%s" % info
        magnet2torrent(info)




if __name__ == "__main__":
    pass
    # startDht()
    #
    # f = file("infohash.txt")
    # findFiles(f)
    # torrent2magnet("0119-sace050.torrent")