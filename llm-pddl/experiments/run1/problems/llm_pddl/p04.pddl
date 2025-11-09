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
    :effect (and (not (on-table ?container)) (holding ?container) (not (on-table ?container)))
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
    :effect (and (empty ?shotglass) (contains-ingredient1 ?shaker) (shaked ?shaker) (not (clean ?shotglass)))
  )

  (:action pour-ingredient2-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)) (clean (hand2)) (unshaked ?shaker) (empty ?shaker))
    :effect (and (empty ?shotglass) (contains-ingredient2 ?shaker) (shaked ?shaker) (not (clean ?shotglass)))
  )

  (:action pour-ingredient3-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (not (empty ?shotglass)) (clean (hand2)) (unshaked ?shaker) (empty ?shaker))
    :effect (and (empty ?shotglass) (contains-ingredient3 ?shaker) (shaked ?shaker) (not (clean ?shotglass)))
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

  (:action pour-cocktail1-to-shotglass1
    :parameters ()
    :precondition (and (empty shot1) (shaked contains-cocktail1 ?shaker) (clean shot1))
    :effect (and (contains-cocktail1 shot1) (not (shaked contains-cocktail1 ?shaker)) (not (clean shot1)))
  )

  (:action pour-cocktail2-to-shotglass3
    :parameters ()
    :precondition (and (empty shot3) (shaked contains-cocktail2 ?shaker) (clean shot3))
    :effect (and (contains-cocktail2 shot3) (not (shaked contains-cocktail2 ?shaker)) (not (clean shot3)))
  )

  (:action pour-cocktail3-to-shotglass2
    :parameters ()
    :precondition (and (empty shot2) (shaked contains-cocktail3 ?shaker) (clean shot2))
    :effect (and (contains-cocktail3 shot2) (not (shaked contains-cocktail3 ?shaker)) (not (clean shot2)))
  )
)

(define (init)
  (and
    (on-table shaker)
    (empty shaker)
    (clean shaker)
    (on-table shot1)
    (empty shot1)
    (clean shot1)
    (on-table shot2)
    (empty shot2)
    (clean shot2)
    (on-table shot3)
    (empty shot3)
    (clean shot3)
    (holding (hand1))
    (holding (hand2))
    (not (contains-ingredient1 shaker))
    (not (contains-ingredient2 shaker))
    (not (contains-ingredient3 shaker))
    (not (contains-cocktail1 shaker))
    (not (contains-cocktail2 shaker))
    (not (contains-cocktail3 shaker))
  )
)

(define (goal)
  (and
    (contains-cocktail1 shot1)
    (contains-cocktail3 shot2)
    (contains-cocktail2 shot3)
  )
)