# Investigating lag spikes

Spark and Observable are already included. Capture the problem before changing several mods or JVM settings at once.

1. Let the world and JEI finish loading, then reproduce the problem during ordinary play. Note what you were doing and the clock time.
2. Press F3. Watch FPS and memory usage during the freeze. Check `/spark tps` for simulation lag; a healthy world targets 20 TPS with ticks below 50 ms.
3. For world freezes, run `/spark tickmonitor --threshold-tick 100`, then `/spark profiler start --only-ticks-over 100 --timeout 120`. Reproduce the spike during those two minutes. Open the resulting profile link and share it with the action and time. Run `/spark tickmonitor` again to stop its messages.
4. For FPS or menu freezes while the world remains healthy, run `/sparkc profiler start --timeout 120` and reproduce the freeze. Client and server profiles measure different threads; capture both when uncertain.
5. To investigate pauses from memory collection, toggle `/spark gcmonitor`. Correlate its reports with the freeze. Toggle it again when finished. Watch whether F3 memory repeatedly fills and drops at the same moment.

Server commands need operator or Spark permissions. On a local test world without cheats, temporarily opening to LAN with cheats allows the server commands. Client `/sparkc` commands do not require server operator access. Record locally with `/spark profiler stop --save-to-file` if you prefer a saved profile instead of the normal upload; consult the command help for the corresponding client option.

Start a comparison with shaders disabled, render distance 8–10, simulation distance 6, and approximately 8 GB allocated if your computer has enough memory. Leave room for Windows and other applications. More allocated memory is not automatically faster. Preserve your current options so changes can be compared one at a time.
