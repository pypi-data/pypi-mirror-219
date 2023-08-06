# Time-Zap

Simple Python CLI for printing time in multiple time zones.

```bash
pop-os:$ time-zap
-------------------
CDT 06:22:16 -05:00
-------------------
UTC 11:22:16 +00:00
EDT 07:22:16 -04:00
MDT 05:22:16 -06:00
PDT 04:22:16 -07:00
-------------------
```

```bash
pop-os:$ time-zap 1337
-------------------
CDT 13:37:00 -05:00
-------------------
UTC 18:37:00 +00:00
EDT 14:37:00 -04:00
MDT 12:37:00 -06:00
PDT 11:37:00 -07:00
-------------------
```

Help:
```bash
pop-os:$ time-zap --help
Usage: time-zap [OPTIONS] [TIME]

  Simple Python CLI for printing time in multiple time zones.

Options:
  --help  Show this message and exit.
```