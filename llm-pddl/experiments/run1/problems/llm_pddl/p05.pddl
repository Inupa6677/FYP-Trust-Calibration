(define (domain robot_barman)
  (:requirements :strips :equality)

  (:predicates
    (on-table ?container)
    (empty ?container)
    (clean ?container)
    (contains-ingredient1 ?container)
    (contains-ingredient2 ?container)
    (contains-ingredient3 ?container)
    (contains-cocktail1 ?shotglass)
    (contains-cocktail2 ?shotglass)
    (contains-cocktail3 ?shotglass)
    (contains-cocktail4 ?shotglass)
  )

  (:action grasp-container
    :parameters (?container)
    :precondition (and (on-table ?container) (not (empty-hand)))
    :effect (and (not (on-table ?container)) (empty-hand) (holding ?container))
  )

  (:action leave-container
    :parameters (?container)
    :precondition (and (holding ?container))
    :effect (and (on-table ?container) (not (holding ?container)) (empty-hand))
  )

  (:action fill-shotglass-with-ingredient1
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient1 ?shotglass)))
    :effect (and (not (empty ?shotglass)) (contains-ingredient1 ?shotglass) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient2
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient2 ?shotglass)))
    :effect (and (not (empty ?shotglass)) (contains-ingredient2 ?shotglass) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient3
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient3 ?shotglass)))
    :effect (and (not (empty ?shotglass)) (contains-ingredient3 ?shotglass) (not (clean ?shotglass)))
  )

  (:action refill-shotglass-with-ingredient1
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (contains-ingredient2 ?shotglass))
    :effect (and (not (empty ?shotglass)) (contains-ingredient1 ?shotglass) (not (clean ?shotglass)))
  )

  (:action refill-shotglass-with-ingredient2
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (contains-ingredient1 ?shotglass))
    :effect (and (not (empty ?shotglass)) (contains-ingredient2 ?shotglass) (not (clean ?shotglass)))
  )

  (:action empty-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-beverage ?shotglass))
    :effect (and (empty ?shotglass) (not (contains-beverage ?shotglass)))
  )

  (:action clean-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (not (holding anything else)) (empty-hand))
    :effect (and (clean ?shotglass) (empty ?shotglass) (empty-hand))
  )

  (:action pour-ingredient1-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-ingredient1 ?shotglass) (empty-shaker) (clean-shaker))
    :effect (and (not (contains-ingredient1 ?shotglass)) (contains-ingredient1 shaker) (shaker (level 1)))
  )

  (:action pour-ingredient2-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-ingredient2 ?shotglass) (empty-shaker) (clean-shaker))
    :effect (and (not (contains-ingredient2 ?shotglass)) (contains-ingredient2 shaker) (shaker (level 1)))
  )

  (:action pour-ingredient3-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-ingredient3 ?shotglass) (empty-shaker) (clean-shaker))
    :effect (and (not (contains-ingredient3 ?shotglass)) (contains-ingredient3 shaker) (shaker (level 1)))
  )

  (:action empty-shaker
    :parameters ()
    :precondition (and (holding shaker) (contains-beverage shaker))
    :effect (and (empty shaker) (not (contains-beverage shaker)))
  )

  (:action clean-shaker
    :parameters ()
    :precondition (and (holding shaker) (empty shaker) (not (holding anything else)) (empty-hand))
    :effect (and (clean shaker) (empty shaker) (empty-hand))
  )

  (:action shake-cocktail
    :parameters ()
    :precondition (and (contains-ingredient1 shaker) (contains-ingredient2 shaker) (not (shaked shaker)) (empty-hand))
    :effect (and (shaked shaker) (contains-cocktail1 shaker) (contains-cocktail2 shaker) (shaker (level 0)))
  )

  (:action pour-cocktail1-to-shotglass1
    :parameters ()
    :precondition (and (shaked shaker) (contains-cocktail1 shaker) (empty shot1) (clean shot1))
    :effect (and (not (shaked shaker)) (contains-cocktail1 shot1) (shaker (level -1)) (not (clean shot1)) (not (empty shot1)))
  )

  (:action pour-cocktail2-to-shotglass4
    :parameters ()
    :precondition (and (shaked shaker) (contains-cocktail2 shaker) (empty shot4) (clean shot4))
    :effect (and (not (shaked shaker)) (contains-cocktail2 shot4) (shaker (level -1)) (not (clean shot4)) (not (empty shot4)))
  )

  (:action pour-cocktail3-to-shotglass3
    :parameters ()
    :precondition (and (shaked shaker) (contains-cocktail3 shaker) (empty shot3) (clean shot3))
    :effect (and (not (shaked shaker)) (contains-cocktail3 shot3) (shaker (level -1)) (not (clean shot3)) (not (empty shot3)))
  )

  (:action pour-cocktail4-to-shotglass2
    :parameters ()
    :precondition (and (shaked shaker) (contains-cocktail4 shaker) (empty shot2) (clean shot2))
    :effect (and (not (shaked shaker)) (contains-cocktail4 shot2) (shaker (level -1)) (not (clean shot2)) (not (empty shot2)))
  )
)

(define (problem robot_barman_problem)
  (:domain robot_barman)
  (:objects shaker1 shaker1-3 shotglass1-5 ingredient1 ingredient2 ingredient3 cocktail1 cocktail2 cocktail3 cocktail4
           - container
           )
  (:init
    (and (on-table shaker1) (empty shaker1) (clean shaker1) (empty-hand)
         (on-table shotglass1) (empty shotglass1) (clean shotglass1)
         (on-table shotglass2) (empty shotglass2) (clean shotglass2)
         (on-table shotglass3) (empty shotglass3) (clean shotglass3)
         (on-table shotglass4) (empty shotglass4) (clean shotglass4)
         )
    (contains-ingredient1 shaker1)
    (contains-ingredient2 shaker1)
    (contains-ingredient1 shotglass5)
    (contains-ingredient2 shotglass5)
  )
  (:goal (and (contains-cocktail1 shot1) (contains-cocktail4 shot2) (contains-cocktail3 shot3) (contains-cocktail2 shot4)))
)