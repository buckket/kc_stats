#!/usr/bin/env python3


from database import create_tables, add_imageboards


data = {
    'krautchan': [
        'b',
        'int',
        'vip'
    ]
}


if __name__ == '__main__':
    create_tables()
    add_imageboards(data)
