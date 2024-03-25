# -*- coding = utf-8 -*-

from pybloom_live import ScalableBloomFilter, BloomFilter


def init_bloom(size=2e8):
    bloom = BloomFilter(capacity=size)
    return bloom
