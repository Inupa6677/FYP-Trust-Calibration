(define (problem p01)
  (:domain barman)
  (:objects
    left right - hand
    l0 l1 l2 - level
    dispenser1 dispenser2 - dispenser
    shaker1 - shaker
    shot1 shot2 - shot
    ingredient1 ingredient2 - ingredient
    cocktail1 - cocktail
  )
  (:init
    (ontable shaker1)
    (ontable shot1)
    (ontable shot2)

    (handempty left)
    (handempty right)

    (clean shaker1) (empty shaker1)
    (clean shot1) (empty shot1)
    (clean shot2) (empty shot2)

    (shaker-empty-level shaker1 l0)
    (shaker-level shaker1 l0)
    (next l0 l1)
    (next l1 l2)

    (unshaked shaker1)

    (dispenses dispenser1 ingredient1)
    (dispenses dispenser2 ingredient2)

    (cocktail-part1 cocktail1 ingredient1)
    (cocktail-part2 cocktail1 ingredient2)
  )
  (:goal (and
    (contains shot1 cocktail1)
  ))
)
