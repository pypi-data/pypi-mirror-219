from datetime import datetime
from typing import Any, Callable, Coroutine, TypeVar

from croniter import CroniterBadCronError, croniter

from amethyst.widget.abc import AmethystPlugin, Callback, CallbackWidget

__all__ = ("AmethystSchedule", "schedule")

PluginT = TypeVar("PluginT", bound=AmethystPlugin)

ScheduleCallback = Callback[PluginT, [], Coroutine[Any, Any, None]]


class AmethystSchedule(CallbackWidget[PluginT, [], Coroutine[Any, Any, None]]):
    """Represents an asynchronous function that should be called on a schedule.

    These are not usually created manually, instead they are created using the `amethyst.schedule` decorator.
    """

    def __init__(
        self,
        cron: str,
        callback: ScheduleCallback[PluginT],
        name: str | None = None,
    ) -> None:
        """Represents an asynchronous function that should be called on a schedule.

        These are not usually created manually, instead they are created using the `amethyst.schedule` decorator.

        Parameters
        ----------
        cron : `str`
            The cron expression to run this schedule on.
        callback : `Callable[[PluginT], T] | Callable[[], Coroutine[Any, Any, T]]`
            The function that should be invoked when this schedule is run.
        name : `str`, optional
            The name of this schedule widget, by default None

        Raises
        ------
        TypeError
            Raised when the provided cron expression is invalid.
        """
        super().__init__(callback, name)
        # validate cron expression
        try:
            croniter(cron)
        except CroniterBadCronError as e:
            raise TypeError(f"Bad Cron Expression '{cron}'") from e
        self._cron = cron

    @property
    def cron(self) -> str:
        """The cron expression for this schedule."""
        return self._cron

    def next_occurrence(self) -> datetime:
        """Gets the next occurrence of this schedule.

        Returns
        -------
        `datetime`
            The `datetime` representing when this schedule should next be called.
        """
        iter = croniter(self.cron, datetime.now())
        return iter.get_next(datetime)


def schedule(cron: str) -> Callable[[ScheduleCallback[PluginT]], AmethystSchedule[PluginT]]:
    """Decorator to designate a regular function to be called on a schedule.

    Parameters
    ----------
    cron: `str`
        The cron expression to run the schedule on.
    """

    def decorator(func: ScheduleCallback[PluginT]) -> AmethystSchedule[PluginT]:
        return AmethystSchedule(cron, func)

    return decorator
