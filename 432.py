from typing import Dict

DEBUG = False

# Bucket forms double linked list too
class Bucket:
    # __slots__ = ("count", "keys", "prev", "next")

    def __init__(self, count:int):
        self.count = count
        self.keys = set[str]()

        self.prev = None
        self.next = None

    def addkey(self, key:str):
        self.keys.add(key)

    def delKey(self, key:str):
        self.keys.discard(key)

    def getAKey(self):
        if not self.keys:
            raise Exception(f"bucket (count={self.count}) has empty keys!")
        else:
            if DEBUG:
                print(f"        getAKey bucket count={self.count} keys={self.getKeyList()}")
            return next(iter(self.keys))

    def getKeyList(self):
        return list(self.keys)


class AllOne:

    def __init__(self):
        self.bucketMap:Dict[str, Bucket] = {}

        self.head = Bucket(0)
        self.tail = Bucket(0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def print(self):
        print(f"bucketMap:")
        for key in self.bucketMap:
            bucket = self.bucketMap[key]
            print(f"    key={key} bucket count={bucket.count} keys={bucket.getKeyList()}")
        print(f"bucket forward linked list:")
        p = self.head
        while p is not None:
            print(f"    bucket count={p.count} keys={p.getKeyList()}")
            p = p.next

        print(f"bucket backward linked list:")
        p = self.tail
        while p is not None:
            print(f"    bucket count={p.count} keys={p.getKeyList()}")
            p = p.prev


    def insertBucketBefore(self, newBucket:Bucket, atBucket:Bucket):
        prevBucket = atBucket.prev

        newBucket.next = atBucket
        newBucket.prev = prevBucket
        atBucket.prev = newBucket
        prevBucket.next = newBucket

    def deleteBucket(self, oldBucket:Bucket):
        oldBucket.prev.next = oldBucket.next
        oldBucket.next.prev = oldBucket.prev
        oldBucket.next = None
        oldBucket.prev = None

    def inc(self, key: str) -> None:
        bucket = self.bucketMap.get(key)
        if bucket is None:
            firstBucket = self.head.next
            if firstBucket != self.tail and firstBucket.count == 1:
                self.head.next.addkey(key)
                self.bucketMap[key] = firstBucket
            else:
                newBucket = Bucket(1)
                newBucket.addkey(key)

                self.bucketMap[key] = newBucket
                if DEBUG:
                    print(f"    insert newBucket at front")
                self.insertBucketBefore(newBucket, self.head.next)
        else:
            count = bucket.count + 1
            bucket.delKey(key)
            nextBucket = bucket.next
            if nextBucket != self.tail and nextBucket.count == count:
                nextBucket.addkey(key)
                self.bucketMap[key] = nextBucket

            else:
                newBucket = Bucket(count)
                newBucket.addkey(key)
                self.bucketMap[key] = newBucket
                self.insertBucketBefore(newBucket, nextBucket)

            if not bucket.keys:
                self.deleteBucket(bucket)

    def dec(self, key: str) -> None:
        bucket = self.bucketMap.get(key)
        if bucket is None:
            return

        count = bucket.count - 1
        bucket.delKey(key)

        if count == 0:
            # Removes the key from the bucket map when its count reaches zero
            del self.bucketMap[key]
        else:
            prevBucket = bucket.prev
            if prevBucket != self.head and prevBucket.count == count:
                prevBucket.addkey(key)
                self.bucketMap[key] = prevBucket
            else:
                newBucket = Bucket(count)
                newBucket.addkey(key)
                self.bucketMap[key] = newBucket
                self.insertBucketBefore(newBucket, bucket)

        if not bucket.keys:
            self.deleteBucket(bucket)


    def getMaxKey(self) -> str:
        if self.head.next == self.tail:
            if DEBUG:
                print(f"        getMaxKey: self.head.next == self.tail")
            return ''
        return self.tail.prev.getAKey()

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            if DEBUG:
                print(f"        getMinKey: self.head.next == self.tail")
            return ''
        return self.head.next.getAKey()


if __name__ == "__main__":
    # Your AllOne object will be instantiated and called as such:
    obj = AllOne()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"empty AllOne object  minKey={minKey} maxKey={maxKey}\n")

    obj.inc("key1")
    obj.print()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"single AllOne object  minKey={minKey} maxKey={maxKey}\n")

    obj.inc("key1")
    obj.print()
    print(f"double AllOne object  minKey={minKey} maxKey={maxKey}\n")

    obj.inc("key2")
    obj.inc("key2")
    obj.inc("key2")
    obj.inc("key2")
    obj.print()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"6 AllOne object  minKey={minKey} maxKey={maxKey}\n")


    obj.dec("key2")
    obj.dec("key2")
    # obj.dec("key2")
    obj.print()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"4 AllOne object  minKey={minKey} maxKey={maxKey}\n")


    obj.dec("key2")
    obj.print()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"3 AllOne object  minKey={minKey} maxKey={maxKey}\n")

    obj.dec("key2")
    obj.print()
    maxKey = obj.getMaxKey()
    minKey = obj.getMinKey()
    print(f"back to 2 AllOne object  minKey={minKey} maxKey={maxKey}\n")

    # # obj.dec(key)
    # param_3 = obj.getMaxKey()
    # param_4 = obj.getMinKey()
