# WebActogram
🌐🏃Actogram from browsers history, may help to retrospectively screen 🌙🛌sleep-wake patterns & disorders!

## Description
Python 3 tool to generate a web actogram from web browsers history files.

To screen sleep-wake patterns and disorders, all tools require that the user wear an actigraphic device or record themselves a sleep diary.

The web actogram is the first pseudo-actigraphic tool that can provide an instantaneous estimation of the user’s sleep-wake pattern, aka actogram, by inferring an actogram from the browser’s history. This could allow for mass screening of sleep-wake patterns and disorders.

The limitations are however as follows:

* The sleep patterns are only very indirectly estimated, only the wakefulness patterns can be considered reliable.
* The web actogram reliability depends on whether the user is an avid user of web browsers: they must use their web browsers on a daily basis.
* The user must use solely one browser, otherwise it won’t work (in the future we will merge multiple browsers’ histories).
* The user must primarily use a web browser on a computer (not on a smartphone - this will be implemented in the future).
* The more data over a longer period, the more precisely and robust the pattern will appear.

How the actogram is plotted was inspired by [this UCSD tutorial](https://ccb.ucsd.edu/the-bioclock-studio/education-resources/basics/part2.html) and [this scientific paper](https://doi.org/10.1186/1741-7007-8-93).

## Install & Quickstart

Install with:

```pip install webactogram```

Use in a terminal (or `cmd` on Windows):

```webactogram```

Note: First, you need to `cd` in a folder with write permission.

This will create a folder `actograms` in the current folder, and add inside a picture with the latest actogram and a csv file with all the browsers activities recorded.

More options, such as the sampling frequency (and hence granularity of the actogram and its patterns) can be shown with:

```webactogram --help```

### Compatibility
Currently configured to import history from ALL browsers available on the system, from the default user profiles for each:
- Windows:
  - Chrome ``History`` file
  - Edge ``History`` file
  - Firefox ``History`` file
- MacOS:
  - Chrome ``History`` file
  - Safari ``History.db``
  - Firefox ``History`` file
- Linux:
  - Firefox ``History`` file

Currently, this script may not function as intended if you use multiple profiles within one browser (especially for Firefox), or the browser's default installation profile has changed.

## Usage
History files are copied from their home directories to a temporary location in the working directory. These copies are then deleted after the script has executed. Only the ``last_visit_time`` is read.

Plots are easily generated from the command line:

```webactogram```

Plots will be saved in a new sub-folder called "actograms" with appropriate timestamp and description. 


Script now supports command line arguments for additional customizability.
For example: 

```python actogram.py --freq '15T' --daily_blur 3 --start '2020-01-01' ```

```python actogram.py --freq '30T' --printer_friendly True```

```python actogram.py --dims (8,8)```

Where: 

```
--freq determines the granularity of binned online/offline periods (default is 15 minutes increments, ex.  --freq '15T')

--start_date sets initial date to plot from, default is 180 days ago (ex. --start_date '2022-01-01')

--daily_blur applies median filtering between days (off by default, ex. --daily_blur 3)  

--period_blur applies median filtering between binned time periods (off by default, ex. --period_blur 5)

--normalize normalizes search frequency against max, then applies binary mask (plot shows periods of some search history vs. none, on by default)

--dims sets the relative dimensions of generated actogram plot (ex. --dims (4, 6))

--printer_friendly sets whether activity is shown in black on white (friendly) or vice versa (False by default, ex. --printer_friendly True)
```

## Latest updates

[Feature] Added support for the ``Default`` profile of Microsoft Edge for Windows

[Bug fix] Previously there was an artificially low minimum window for all generated plots. Plots can now be shown with minutes resolution 

[Feature] Added "activity CDF" subplot to gauge periods of minimum and maximum activity 

[Feature] Added cumulative "offline hours" subplot to estimate sleep per 24h period (NB: this yields artificially high results with high freq values)

## Authors

This tool is a fork from the excellent [online_actogram](https://github.com/barrettfdavis/online_actogram) script by Barrett F. Davis who conceived both the idea and the first implementation initially released in [July 2020](https://web.archive.org/web/20221127100155/https://www.reddit.com/r/N24/comments/hxve2w/dont_delete_your_browser_history/).

## License

MIT Public License.

## Similar projects

Another project, inspired by this one, was written in Javascript using D3, but it cannot fetch browser's history: [Tylian's D3 Browser's History](https://web.archive.org/web/20221207124930/https://tylian.net/d3/history.html).
How to generate the history.txt file ([source](https://www.reddit.com/r/N24/comments/hxve2w/comment/g30ve2y/?utm_source=share&utm_medium=web2x&context=3)): ```It's a dump of the timestamp column with some manual processing to divide every entry by 1000, since Firefox stores them as a nanosecond epoch for some reason..```
