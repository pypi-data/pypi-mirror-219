from __future__ import annotations

from asyncio import CancelledError, _get_running_loop
from collections import deque
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from threading import Lock

if TYPE_CHECKING:
    from types import TracebackType
    from asyncio import AbstractEventLoop, Future
    from typing import Callable, Deque, Literal, Optional, Tuple, Type

__all__: Tuple[str, ...] = (
    'Throttler',
)

class Throttler:
    """
    Throttled lock implementation.

    Inspired by the Lock and BoundedSemaphore classes in the asyncio library.

    Implements the leaky bucket algorithm by only allowinng a limited number
    of acquires over a given interval. If no slots are available when an acquire
    is requested, the request will be blocked until a slot becomes available.
    """
    if TYPE_CHECKING:
        __lock: Lock # internal lock
        _lock_waiters: Optional[Deque[Future[Literal[True]]]]
        _slot_waiters: Optional[Deque[Future[Literal[True]]]]
        _expiry: Optional[Deque[datetime]]
        _locked: bool
        _limit: int
        _value: int
        _interval: timedelta
        _loop: Optional[AbstractEventLoop]

    def __init__(
        self: Throttler,
        *,
        limit: Optional[int] = 1,
        interval: timedelta = timedelta(seconds = 1),
    ) -> None:
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")

        if limit < 0:
            raise ValueError("Semaphore initial value must be >= 0")

        if not isinstance(interval, timedelta):
            raise TypeError("interval must be a timedelta")

        self._lock = Lock()
        self._lock_waiters = None
        self._slot_waiters = None
        self._locked = False
        self._limit = limit
        self._value = self._limit
        self._interval = interval

    def __repr__(self: Throttler) -> str:
        res = super().__repr__()

        with self.__lock:
            # collect values under the global lock
            # so their values are assured
            locked = self._locked
            slot_waiters = self.slot_waiters
            lock_waiters = self.lock_waiters
            available = self._value
            limit = self._limit

        extra = f"{'locked' if locked else 'unlocked'}, available={available!r} limit={limit!r}"

        if slot_waiters > 0:
            extra += f', slot_waiters={slot_waiters!r}'

        if lock_waiters > 0:
            extra += f', lock_waiters={lock_waiters!r}'

        return f'<{res[1:-1]} {extra}>'

    async def __aenter__(self: Throttler) -> None:
        """
        Await until a lock is acquired.

        """
        await self.acquire()

    async def __aexit__(
        self: Throttler,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        """
        Release the lock.

        """
        self.release()

    def _get_loop(self: Throttler):
        loop = _get_running_loop()

        with self.__lock:
            if self._loop is None:
                self._loop = loop

        if loop is not self._loop:
            raise RuntimeError(f'{self!r} is bound to a different event loop')

        return loop

    @property
    def locked(self: Throttler) -> bool:
        """
        Return True if lock is acquired.

        """
        return self._locked

    @property
    def lock_queue(self: Throttler) -> int:
        """
        Returns the number of waiters for the lock. 

        """
        return len(self._lock_waiters) # type: ignore[arg-type]

    @property
    def unlocked(self: Throttler) -> bool:
        """
        Return True if lock is not acquired.

        """
        return not self._locked

    @property
    def full(self: Throttler) -> bool:
        """
        Returns True if no slots are available.

        """
        return self._value == 0

    @property
    def slot_queue(self: Throttler) -> int:
        """
        Returns the number of waiters for a slot.

        """
        return len(self._slot_waiters) # type: ignore[arg-type]

    @property
    def slot_time(self: Throttler) -> timedelta:
        """
        Return an estimated time until a slot is available.

        """
        # if slots are available, there will be no wait time
        if not self.full:
            return timedelta(seconds = 0)

        # when there are no waiters, the only wait time
        # will be equal to now - soonest_expiry
        now = datetime.utcnow()

        with self.__lock:
            soonest = self._expiry[0] # type: ignore[index]
            waiters = self.slot_waiters
            interval = self._interval

        if waiters == 0:
            return timedelta(soonest - now) # type: ignore[arg-type]

        # otherwise, the wait time will be equal to
        # the soonest expiry, plus the time interval
        # multiplied by the number of waiters

        # while this is a reliable method to check when a slot
        # will become available, it is not accurate, as waiters
        # may be cancelled while waiting, and new waiters may
        # be appended to the cache immediately after this property
        # is accessed. this is a limitation of the leaky bucket
        # algorithm, and is not a bug in the implementation.
        return timedelta((soonest - now) + (interval * waiters)) # type: ignore[arg-type]

    @property
    def filling(self: Throttler) -> bool:
        """
        Returns true if there are slots both
        taken and available.

        A True response indicates a non-zero state
        where slots have been taken, but slots are
        still available to be acquired.

        """
        return 0 < self._value < self._limit

    @property
    def slot_waiters(self: Throttler) -> int:
        """
        Returns the number of waiters for a slot.

        """
        return len(self._slot_waiters) # type: ignore[arg-type]

    @property
    def lock_waiters(self: Throttler) -> int:
        """
        Returns the number of waiters for the lock.

        """ 
        return len(self._lock_waiters) # type: ignore[arg-type]

    @property
    def empty(self: Throttler) -> bool:
        """
        Returns True if all slots are available.

        """
        return self._value == self._limit

    def _wake_up_waiter(
        self: Throttler,
        cache: deque,
    ) -> None:
        """
        Wake up the first waiter in the provided cache, if it isn't done.
        
        """
        if not cache:
            return

        # a for-loop is used, but only one valid entry will have a result
        # set on it. Once a valid entry is found and the result set, the
        # loop will be broken.
        for fut in cache:
            # .done() means that a waiter will wake up later on and
            # either take the lock, or, if it was cancelled and lock wasn't
            # taken already, will hit this again and wake up a new waiter.
            if fut.done():
                continue

            fut.set_result(True)
            break

    def _fill(self: Throttler) -> None:
        """
        Decrement the number of available slots by one.

        """
        if self._value == 0:
            raise RuntimeError('All slots have already been acquired.')

        self._value -= 1
        now = datetime.now()
        then = now + self._interval
        self._expiry.append(then) # type: ignore[union-attr]

        self._get_loop().call_at(then, lambda: self._empty(then))

    def _empty(self: Throttler, expiry: datetime) -> None:
        """
        Increment the number of available slots by one.

        """
        if self._value == self._limit:
            raise RuntimeError('No slots have been acquired.')

        self._value += 1

        # ensure the related expiry object is removed
        # so the slot_time property can return an accurate
        # value of when a slot will become available
        self._expiry.remove(expiry) # type: ignore[union-attr]

        self._wake_up_waiter(self._slot_waiters) # type: ignore[arg-type]

    def _lock(self: Throttler) -> None:
        """
        Acquire the lock.

        """
        if self._locked:
            raise RuntimeError('Lock is already acquired.')

        self._locked = True

    def _unlock(self: Throttler) -> None:
        """
        Release the lock.

        """
        if not self._locked:
            raise RuntimeError('Lock is not acquired.')

        self._locked = False

        self._wake_up_waiter(self._lock_waiters) # type: ignore[arg-type]

    async def _acquire(
        self: Throttler,
        cache: deque,
        check: bool,
        action: Callable[..., None],
    ) -> None:
        """
        If a boolean value is true, Await until a future is woken up, then
        perform an action.

        This prevents code bloat by allowing us to perform the same
        action many times without having to write the same code over and
        over again.

        """
        flag = True

        # the while loop allows us to continue to attempt
        # the acquire operation until it is either cancelled
        # or successfully acquired
        while flag:
            # if the provided check value is true,
            # then the caller expects to wait until
            # its value is expected to be false
            # the caller manages the cache where the
            # future will be stored, and we expect it to
            # handle dispatching the wake-up signal as well
            if check:
                # create a future that will receive the wake-up signal,
                # which will see its result set to True
                fut = self._get_loop().create_future()

                with self.__lock:
                    # append the future to the provided cache
                    # so it can receive future wake-up signals
                    cache.append(fut)

                # now, wait for the signal to be received
                # if it is cancelled along the way, then
                # it will be removed and the action will
                # not be performed
                try:
                    await fut
                except CancelledError:
                    # setting the flag here will tell the
                    # remaining code not to perform the provided
                    # action and to end the while loop
                    # this is an unfortunate side-effect of
                    # having to call the provided action regardless
                    # of the check value
                    flag = False
                finally:
                    with self.__lock:
                        # remove the future from the cache
                        cache.remove(fut)

            # if the future was cancelled, we don't want to
            # perform the resulting action, so check that first
            if not flag:
                # the action should be performed even if the check
                # value is False, since it is expected to be performed
                # to be performed once the check value would return False
                try:
                    # since the global lock is used to perform the action
                    # a RuntimeError should never be raised, but we run
                    # it in a try/except block just in case, since the
                    # actions passed to this method are expected to raise
                    # RuntimeErrors when an exception occurs
                    with self.__lock:
                        action()
                except RuntimeError:
                    # a failure is expected to occur if the action
                    # occurred at an inappropriate time, so we just
                    # need to try again
                    continue
                else:
                    # otherwise, the action was successful and the loop
                    # can end, which will also return the method call
                    break

    async def acquire(self: Throttler) -> None:
        """
        Acquire a lock.

        This method blocks until a slot is available and the lock is acquired.
        """
        with self.__lock:
            # ensure there is a slot waiter cache
            if self._slot_waiters is None:
                self._slot_waiters = deque()

            # ensure there is a lock waiter cache
            if self._lock_waiters is None:
                self._lock_waiters = deque()

        # wait for a slot
        await self._acquire(
            self._slot_waiters,
            self.full,
            self._fill,
        )

        # wait for the lock
        await self._acquire(
            self._lock_waiters,
            self.locked,
            self._lock,
        )

    def release(self: Throttler) -> None:
        """
        Release a lock.

        """
        # use the global lock to ensure only one caller
        # may attempt to unlock the instance at a time
        with self.__lock:
            self._unlock()
