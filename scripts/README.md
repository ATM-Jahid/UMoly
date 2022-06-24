# Workflow

## Main pipeline
- dump > **unwrapper** > unwDump
- unwDump > **sqdi/dump** > sqdi/last
- unwDump & sqdi/last > **buffer** > buff/msd

## Plotting
- sqdi/last > **sqdi/hist** > histogram
