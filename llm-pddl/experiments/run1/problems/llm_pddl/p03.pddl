(define (domain RobotBarman)
  (:requirements :strips :equality)

  (:predicates
    (on-table ?container)
    (empty ?container)
    (clean ?container)
    (contains-ingredient1 ?shotglass)
    (contains-ingredient2 ?shotglass)
    (contains-ingredient3 ?shotglass)
    (contains-cocktail1 ?shotglass)
    (contains-cocktail2 ?shotglass)
    (contains-cocktail3 ?shotglass)
    (unshaked ?shaker)
    (shaked ?shaker)
  )

  (:action grasp-container
    :parameters (?container)
    :precondition (and (on-table ?container) (not (and (holding ?container) (not (empty ?container)))))
    :effect (and (not (on-table ?container)) (holding ?container) (not (empty ?container)))
  )

  (:action leave-container
    :parameters (?container)
    :precondition (holding ?container)
    :effect (and (on-table ?container) (not (holding ?container)) (empty ?container))
  )

  (:action fill-shotglass-with-ingredient1
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (empty ?shotglass)) (contains-ingredient1 ?shotglass) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient2
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (empty ?shotglass)) (contains-ingredient2 ?shotglass) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient3
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (empty ?shotglass)) (contains-ingredient3 ?shotglass) (not (clean ?shotglass)))
  )

  (:action empty-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)))
    :effect (and (empty ?shotglass) (clean ?shotglass))
  )

  (:action clean-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (not (empty (hand2))) (clean ?shotglass))
    :effect (and (clean ?shotglass) (not (holding ?shotglass)))
  )

  (:action pour-ingredient1-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)) (clean (hand2)) (unshaked ?shaker) (empty ?shaker))
    :effect (and (empty ?shotglass) (contains-ingredient1 ?shaker) (shaked ?shaker) (not (clean ?shaker)))
  )

  (:action pour-ingredient2-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)) (clean (hand2)) (unshaked ?shaker) (empty ?shaker))
    :effect (and (empty ?shotglass) (contains-ingredient2 ?shaker) (shaked ?shaker) (not (clean ?shaker)))
  )

  (:action pour-ingredient3-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)) (clean (hand2)) (unshaked ?shaker) (empty ?shaker))
    :effect (and (empty ?shotglass) (contains-ingredient3 ?shaker) (shaked ?shaker) (not (clean ?shaker)))
  )

  (:action empty-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (shaked ?shaker))
    :effect (and (empty ?shaker) (unshaked ?shaker))
  )

  (:action clean-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty ?shaker) (not (empty (hand2))) (unshaked ?shaker))
    :effect (and (clean ?shaker) (not (holding ?shaker)))
  )

  (:action shake-cocktail
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty ?shaker) (unshaked ?shaker) (contains-ingredient1 ?shaker) (contains-ingredient2 ?shaker))
    :effect (and (shaked ?shaker) (not (contains-ingredient1 ?shaker)) (not (contains-ingredient2 ?shaker)) (contains-cocktail1 ?shaker))
  )

  (:action pour-cocktail1-to-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shaker) (shaked ?shaker) (contains-cocktail1 ?shaker) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (shaked ?shaker)) (contains-cocktail1 ?shotglass) (not (clean ?shotglass)) (not (empty (hand2))) (unshaked ?shaker))
  )

  (:action pour-cocktail2-to-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shaker) (shaked ?shaker) (contains-cocktail2 ?shaker) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (shaked ?shaker)) (contains-cocktail2 ?shotglass) (not (clean ?shotglass)) (not (empty (hand2))) (unshaked ?shaker))
  )

  (:action pour-cocktail3-to-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shaker) (shaked ?shaker) (contains-cocktail3 ?shaker) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (shaked ?shaker)) (contains-cocktail3 ?shotglass) (not (clean ?shotglass)) (not (empty (hand2))) (unshaked ?shaker))
  )
)

(define (init)
  (and
    (on-table shaker1)
    (on-table shotglass1)
    (on-table shotglass2)
    (on-table shotglass3)
    (on-table dispenser1)
    (on-table dispenser2)
    (on-table dispenser3)
    (empty shaker1)
    (clean shaker1)
    (empty shotglass1)
    (clean shotglass1)
    (empty shotglass2)
    (clean shotglass2)
    (empty shotglass3)
    (clean shotglass3)
    (holding nil)
    (empty (hand1))
    (empty (hand2))
  )
)

(define (goal)
  (and
    (contains-cocktail1 shot1)
    (contains-cocktail2 shot2)
    (contains-cocktail3 shot3)
  )
)