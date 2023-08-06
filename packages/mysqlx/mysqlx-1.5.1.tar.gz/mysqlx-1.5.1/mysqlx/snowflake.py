import time
from .support import DB_LOCK

_SNOWFLAKE = None
_WORKER_BITS = 10
_SEQUENCE_BITS = 12
_EPOCH = 1688140800000
# _SEQUENCE_MASK = 4095


def init_snowflake(machine_id=1, epoch=_EPOCH, worker_bits=_WORKER_BITS, sequence_bits=_SEQUENCE_BITS):
    global _SNOWFLAKE
    _SNOWFLAKE = Snowflake(machine_id, epoch, worker_bits, sequence_bits)


def get_id():
    global _SNOWFLAKE
    try:
        return _SNOWFLAKE.generate_id()
    except AttributeError:
        raise RuntimeError("Please init Snowflake first with: snowflake.init_snowflake(machine_id: int, epoch: int, worker_bits: int, sequence_bits: int)")


def _get_timestamp():
    return int(time.time() * 1000)


class Snowflake:
    def __init__(self, machine_id: int, epoch: int, worker_bits: int, sequence_bits: int):
        self.machine_id = machine_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.worker_shift = sequence_bits
        self.sequence_mask = -1 ^ (-1 << sequence_bits)
        self.timestamp_left_shift = worker_bits + sequence_bits

        maxWorkerId = -1 ^ (-1 << worker_bits);
        assert 0 < machine_id <= maxWorkerId, 'machine_id must ge 0 le %d' % maxWorkerId
        assert 10 <= self.timestamp_left_shift <= 22, 'worker_bits add sequence_bits must between 10 and 20, but it is %d' % self.timestamp_left_shift

    def generate_id(self):
        with DB_LOCK:
            timestamp = _get_timestamp()
            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards")
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            self.last_timestamp = timestamp
            return ((timestamp - self.epoch) << self.timestamp_left_shift) | (self.machine_id << self.worker_shift) | self.sequence
            # return ((timestamp - 1288834974657) << 22) | (self.machine_id << 12) | self.sequence

    @staticmethod
    def _wait_next_millis(last_timestamp):
        timestamp = _get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = _get_timestamp()
        return timestamp

