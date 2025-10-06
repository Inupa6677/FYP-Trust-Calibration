(define (problem tireworld-1)
(:domain tyreworld)
(:objects
boot - container
jack pump wrench wheel nut hub - obj)
(:predicates
(open ?x)
(closed ?x)
(have ?x)
(in ?x ?y)
(loose ?x ?y)
(tight ?x ?y)
(unlocked ?x)
(on-ground ?x)
(not-on-ground ?x)
(inflated ?x)
(not-inflated ?x)
(fastened ?x)
(unfastened ?x)
(free ?x)
(on ?x ?y)
(intact ?x))

(:init
(in jack boot)
(in pump boot)
(in wrench boot)
(unlocked boot)
(closed boot)
(not-inflated (all wheel))
(on-ground (all hub))
(tight (all nut) (all hub))
(fastened (all hub))
(on (all wheel) (all hub)))

(:goal
(and
(in (all wheel) boot)
(not (on (all wheel) (all hub)))
(on-ground (all hub))
(tight (all nut) (all hub))
(fastened (all hub))
(inflated (all wheel))))
)