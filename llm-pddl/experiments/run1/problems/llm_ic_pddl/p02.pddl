(define (problem tireworld-9)
(:domain tyreworld)
(:objects
boot - container
jack pump wrench - tool
wheel1 wheel2 ... wheel8 - wheel
hub1 hub2 ... hub9 - hub
nut1 nut2 ... nut9 - nut)

(:init
(in jack boot)
(in pump boot)
(in wrench boot)
(unlocked boot)
(closed boot)
(intact wheel1)
(in wheel1 boot)
(not-inflated wheel1)
(intact wheel2)
(in wheel2 boot)
(not-inflated wheel2)
(on wheel3 hub1)
(on-ground hub1)
(tight nut1 hub1)
(fastened hub1)
(on wheel4 hub2)
(on-ground hub2)
(tight nut2 hub2)
(fastened hub2)
...
(on wheel9 hub9)
(on-ground hub9)
(tight nut9 hub9)
(fastened hub9))

(:goal
(and
(on wheel1 hub1)
(inflated wheel1)
(tight nut1 hub1)
(in wheel1 boot)
(on wheel2 hub2)
(inflated wheel2)
(tight nut2 hub2)
(in wheel2 boot)
...
(on wheel8 hub8)
(inflated wheel8)
(tight nut8 hub8)
(in wheel8 boot)
(on wheel9 hub9)
(inflated wheel9)
(tight nut9 hub9)
(in wheel9 boot)
(in wrench boot)
(in jack boot)
(in pump boot)
(closed boot)))
)