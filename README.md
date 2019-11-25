# thingiverse_scraper

Scans Thingiverse.com for active project pages/things and downloads things locally.

TO DO:

- Implement better error handling (ConnectionReset/MemoryErrors are reasonably rare (Only once every couple days). These are purposely handled manually to ensure an obnoxious number of retry requests aren't hammering Thingiverse).
  This doesn't happen often enough to become really bothersome.
- Add user/permissions to SQL script to automate setup.
- Add metrics (Emailed reports, etc.) when disk hits % full benchmarks to ensure servers don't overload.
