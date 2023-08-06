import arrow
import click

# TODO set a global time zone config variable here
CONFIGURED_TIME_ZONE = "US/Central"
CONFIGURED_TIME_ZONE_LIST = ["UTC", "US/Eastern", "US/Mountain", "US/Pacific"]


@click.command()
@click.argument("time", default="now")
def main(time):
    """Simple Python CLI for printing time in multiple time zones."""
    if check_time(time):
        click.echo(echo_time(make_time(time)))
    else:
        click.echo(echo_error(time))


def make_time(time, zone=CONFIGURED_TIME_ZONE):
    """Takes 24hr time arguement and returns a time object."""
    time_now = arrow.now(tz=zone)
    year = time_now.year
    month = time_now.month
    day = time_now.day

    if time == "now":
        return time_now
    else:
        hour = int(time[:2])
        minute = int(time[2:])
        return arrow.get(year, month, day, hour, minute, tzinfo=zone)


def echo_time(time, zone_list=CONFIGURED_TIME_ZONE_LIST):
    """Convert time to different timezones and construct message."""
    format = "ZZZ HH:mm:ss ZZ"
    time_str = time.format(format)

    msg = "-" * len(time_str) + "\n" + time_str + "\n" + "-" * len(time_str) + "\n"
    msg += "\n".join([time.to(tz=zone).format(format) for zone in zone_list])
    msg += "\n" + "-" * len(time_str)

    return msg


def echo_error(time):
    return f"Incorrect time: {time}\nEnter time in 24hr 'HHmm' or 'now'."


def check_time(time):
    """Parse time arguement and ensure it is a 24hr time"""
    if time == "now":
        return True
    # TODO shorten this
    elif len(time) == 4 and time.isdigit() and time[:2] < "24" and time[2:] < "60":
        return True
    else:
        return False


if __name__ == "__main__":
    pass
