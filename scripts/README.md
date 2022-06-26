# Workflow

## Main pipeline
- dump > **unwrapper** > unwDump
- unwDump > **sqdi/dump** > sqdi/last
- unwDump & sqdi/last > **buffer** > buff/msd
- buff/msd > **clfMsdLinReg** > clf/slopes
- clf/slopes > **diffuCalc** > diffusivities

## Plotting
- sqdi/last > **sqdi/hist** > histogram
- buff/msd > **clfMsdPlotter** > graph
- buff/msd > **clfMsdLinReg** > linear fit
- diffusivities > **diffuPlotter** > D vs 1/T
