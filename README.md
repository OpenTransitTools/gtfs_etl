# gtfs_etl
----------
**about**: maintain an up-to-date cache of GTFS feeds + ETL and transform scripts

**goals**: automate keeping feeds up-to-date; convert Fares V1 feeds to V2 via the Arcadis tooling; other transform scripts

**notes**: 
 - ?

### installation 
- pip install poetry
- git clone https://github.com/OpenTransitTools/gtfs_etl.git
- cd gtfs_etl
- git update-index --assume-unchanged poetry.lock
- poetry install

### applications
 - poetry run gtfs-update

