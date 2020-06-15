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
