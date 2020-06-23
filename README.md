**SAPMA**

_How to run_

`pipenv run python main.py --start_ts 01-05-2015 --end_ts 31-08-2019 --step 60 --inversion_layer 600 --source_data ships.xlsx --measurements_data Geiranger_2015_2019_measurements.xlsx --station '[\"G\"]' --pm_type PM1`


Input
- Timeframe 
- Timestep
- Initial concentration
- 

Output
- Final PM concentration
- Build-up over time
- Compare to measurements taken in that timeframe


Excel with ships containing
- TAB = Time in harbour
- GRT = Volume in tons (according to which we divide into big/small group)

Formula for calculating the emmisions + static values (include time)

Volume of GeoTIFF 

Model
- Timestep every interval
- Determine what ships are in harbor
  - If they were already there
  - If the ship is big or small
- Calculate emmisions for timestep
  - If first timestep for this ship: add timestep of manouvering (to max 0.5 hour summed) and timestep-manouvering of normal emmissions
  - Else 1 timestep of normal emmissions
- Add concentration to running summation of concentration

Send to Ken
- GRT value for big and small ship
  - You will get back PME + PAE
  - Use average for splitting big and small and then average again for the actual GRT value
