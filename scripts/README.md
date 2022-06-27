# Workflow

## Main pipeline
- dumpRun > **unwrapper** > unwDump
- unwDump > **sqdi_dump** > sqdi_last
- unwDump & sqdi_last > **buffer** > buff_msd
- buff_msd > **clfMsdLinReg** > clf_slopes
- clf_slopes > **diffuCalc** > diffusivities

### Xe
- dumpRun > **xe_pos_dump** > xe_pos
- xe_pos > **xe_buff** > xe_msd

## Plotting
- sqdi_last > **sqdi_hist** > histogram
- buff_msd > **clfMsdPlotter** > graph
- buff_msd > **clfMsdLinReg** > linear fit
- diffusivities > **diffuPlotter** > D vs 1/T
