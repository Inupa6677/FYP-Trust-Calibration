(define (problem grid-building)
(:domain termes)

(:objects
    n0 - numb
    n1 - numb
    n2 - numb
    n3 - numb
    n4 - numb
    n5 - numb
    pos-0-0 - position
    pos-0-1 - position
    pos-0-2 - position
    pos-1-0 - position
    pos-1-1 - position
    pos-1-2 - position
    pos-2-0 - position
    pos-2-1 - position
    pos-2-2 - position
)

(:init
    (height pos-0-0 n0)
    (height pos-0-1 n0)
    (height pos-0-2 n0)
    (height pos-1-0 n0)
    (height pos-1-1 n0)
    (height pos-1-2 n0)
    (height pos-2-0 n0)
    (height pos-2-1 n0)
    (height pos-2-2 n0)
    (at pos-2-0)
    (IS-DEPOT pos-2-0)
)

(:goal
    (and
        (height pos-2-1 n5)
        (not (has-block))
    )
)

(:action move
    :parameters (?from - position ?to - position ?h - numb)
    :precondition
    (and
        (at ?from)
        (NEIGHBOR ?from ?to)
        (height ?from ?h)
        (height ?to ?h)
    )
    :effect
    (and
        (not (at ?from))
        (at ?to)
    )
)

(:action move-up
    :parameters (?from - position ?hfrom - numb ?to - position ?hto - numb)
    :precondition
    (and
        (at ?from)
        (NEIGHBOR ?from ?to)
        (height ?from ?hfrom)
        (height ?to ?hto)
        (SUCC ?hto ?hfrom)
    )
    :effect
    (and
        (not (at ?from))
        (at ?to)
    )
)

(:action move-down
    :parameters (?from - position ?hfrom - numb ?to - position ?hto - numb)
    :precondition
    (and
        (at ?from)
        (NEIGHBOR ?from ?to)
        (height ?from ?hfrom)
        (height ?to ?hto)
        (SUCC ?hfrom ?hto)
    )
    :effect
    (and
        (not (at ?from))
        (at ?to)
    )
)

(:action place-block
    :parameters (?rpos - position ?bpos - position ?hbefore - numb ?hafter - numb)
    :precondition
    (and
        (at ?rpos)
        (NEIGHBOR ?rpos ?bpos)
        (height ?rpos ?hbefore)
        (height ?bpos ?hbefore)
        (SUCC ?hafter ?hbefore)
        (has-block)
        (not (IS-DEPOT ?bpos))
    )
    :effect
    (and
        (not (height ?bpos ?hbefore))
        (height ?bpos ?hafter)
        (not (has-block))
    )
)

(:action remove-block
    :parameters (?rpos - position ?bpos - position ?hbefore - numb ?hafter - numb)
    :precondition
    (and
        (at ?rpos)
        (NEIGHBOR ?rpos ?bpos)
        (height ?rpos ?hafter)
        (height ?bpos ?hbefore)
        (SUCC ?hbefore ?hafter)
        (not (has-block))
    )
    :effect
    (and
        (not (height ?bpos ?hbefore))
        (height ?bpos ?hafter)
        (has-block)
    )
)

(:action create-block
    :parameters (?p - position)
    :precondition
    (and
        (at ?p)
        (not (has-block))
        (IS-DEPOT ?p)
    )
    :effect
    (and
        (has-block)
    )
)

(:action destroy-block
    :parameters (?p - position)
    :precondition
    (and
        (at ?p)
        (has-block)
        (IS-DEPOT ?p)
    )
    :effect
    (and
        (not (has-block))
    )
)

(:action build-block
    :parameters (?pos - position)
    :precondition
    (and
        (at ?pos)
        (not (height ?pos n5))
        (not (has-block))
    )
    :effect
    (and
        (or (height ?pos (SUCC (height ?pos)))
            (if (= (height ?pos n4) n5)
                (and (height ?pos n5) (not (has-block)))
                (and (height ?pos (SUCC (height ?pos))) (has-block))))
    )
)

(:action remove-unplaced-blocks
    :parameters ()
    :precondition
    (not (has-block))
    :effect
    (and (not (exists (?p - position) (and (position ?p) (not (IS-DEPOT ?p)) (not (height ?p n5))))))
)

)