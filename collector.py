#!/usr/bin/env python3

import datetime
import pykc

from database import Imageboard, Post


def update_stats():
    kc = pykc.Krautchan()
    for imageboard in Imageboard.select():
        for board in imageboard.boards:
            try:
                post_id_new = kc.get_newest_post_id(board.board)
                try:
                    # make sure values are monotonically increasing
                    post_id_old = board.data.select().order_by(Post.timestamp.desc()).get().post_id
                    post_id = post_id_new if post_id_new >= post_id_old else post_id_old
                except Post.DoesNotExist:
                    post_id = post_id_new
                print("New post id for /{}/ on {}: {}".format(
                    board.board, imageboard.imageboard, post_id))
                Post.create(
                    imageboard=imageboard,
                    board=board,
                    timestamp=datetime.datetime.utcnow(),
                    post_id=post_id)
            except Exception as e:
                print("There was en error while fetching data for {} on {}: {}".format(
                    board.board, imageboard.imageboard, repr(e)))


if __name__ == '__main__':
    update_stats()
