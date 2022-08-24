import logging
import sys
from typing import List
from copy import copy
from dataclasses import dataclass
from typing import Optional
from modelexecute.aws import s3_client
import math


@dataclass
class Partition:
    bucket: Optional[str] = None
    key: Optional[str] = None
    offset: Optional[int] = None
    length: Optional[int] = None

    def __init__(self, bucket: str, key: str) -> None:
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        logging.basicConfig()
        self.logger: logging.Logger = logging.getLogger()

    def read(self):

        sys.stdout.write('>>>>>>>>>>>>>>>> Range=' +
                         f'bytes={self.offset}-{self.offset + self.length} <<<<<<<<<<<<<<<<<<<<<')
        sys.stdout.flush()
        return self.s3_client.get_object(Bucket=self.bucket, Key=self.key, Range=f'bytes={self.offset}-{self.offset + self.length}')


class Partitioner:
    def __init__(self, bucket: str, key: str, max_partition_size: int, poke_increment: int) -> None:

        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.object_head = self.s3_client.head_object(
            Bucket=self.bucket, Key=self.key)

        self.total_size = self.object_head['ContentLength']

        self.max_partition_size = max_partition_size

        self.num_of_partitions = math.ceil(
            self.total_size / self.max_partition_size)

        self.estimated_partition_size = math.ceil(
            self.total_size / self.num_of_partitions)

        self.poke_increment = poke_increment

        self.partitions: List[Partition] = []

    def partition(self):
        for i in range(self.num_of_partitions):
            partition: Partition = Partition(bucket=self.bucket, key=self.key)
            if i == 0:
                partition.offset = 0
            else:
                partition.offset = self.partitions[i -
                                                   1].offset + self.partitions[i - 1].length

            newline_not_found = True
            length: int = copy(self.estimated_partition_size)
            if ((partition.offset + length) > self.total_size) or ((partition.offset + length + self.poke_increment) > self.total_size):
                length = self.total_size - partition.offset
            else:
                while newline_not_found:
                    poke_chunk = self.s3_client.get_object(
                        Bucket=self.bucket, Key=self.key, Range=f'bytes={partition.offset + length}-{partition.offset + length + self.poke_increment}')
                    for b in poke_chunk['Body'].read():
                        if b == b'\n'[0]:
                            newline_not_found = False
                            break
                        length = length + 1
            partition.length = length
            if (partition.length > 0):
                self.partitions.append(partition)

    def get_partitions(self):
        return self.partitions
