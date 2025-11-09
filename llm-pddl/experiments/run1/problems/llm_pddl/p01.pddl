(define (domain RobotBarman)
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
  )

  (:action grasp-container
    :parameters (?container)
    :precondition (and (on-table ?container) (not (and (holding ?left-hand) (equal ?container ?left-hand))) (not (and (holding ?right-hand) (equal ?container ?right-hand))))
    :effect (and (not (on-table ?container)) (holding ?container) (not (on-table ?container)))
  )

  (:action leave-container
    :parameters (?container)
    :precondition (and (holding ?container))
    :effect (and (on-table ?container) (not (holding ?container)))
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
    :precondition (and (holding ?shotglass) (contains-beverage ?shotglass))
    :effect (and (empty ?shotglass) (not (contains-beverage ?shotglass)))
  )

  (:action clean-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass))
    :effect (and (clean ?shotglass) (not (empty ?shotglass)))
  )

  (:action pour-ingredient1-to-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-ingredient1 ?shotglass) (empty ?shaker))
    :effect (and (not (contains-ingredient1 ?shotglass)) (contains-ingredient1 ?shaker) (shaker-level +1) (not (clean ?shaker)))
  )

  (:action pour-ingredient1-to-used-shaker
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-ingredient1 ?shotglass) (empty ?shaker) (not (shaker-level = max-level)))
    :effect (and (not (contains-ingredient1 ?shotglass)) (contains-ingredient1 ?shaker) (shaker-level +1) (not (clean ?shaker)))
  )

  (:action empty-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (contains-beverage ?shaker))
    :effect (and (empty ?shaker) (not (contains-beverage ?shaker)))
  )

  (:action clean-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty ?shaker))
    :effect (and (clean ?shaker) (not (empty ?shaker)))
  )

  (:action shake-cocktail
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty ?shaker) (contains-ingredient1 ?shaker) (contains-ingredient2 ?shaker))
    :effect (and (not (empty ?shaker)) (contains-cocktail ?shaker) (shaker-level +1) (not (clean ?shaker)))
  )

  (:action pour-cocktail-to-shotglass
    :parameters (?shaker ?shotglass)
    :precondition (and (holding ?shaker) (contains-cocktail ?shaker) (empty ?shotglass) (clean ?shotglass))
    :effect (and (not (contains-cocktail ?shaker)) (contains-cocktail ?shotglass) (not (clean ?shotglass)) (shaker-level -1))
  )
)

(define (problem RobotBarman-Problem)
  (:domain RobotBarman)
  (:objects shaker1 level1 level2 level3 shotglass1 shotglass2 shotglass3 ingredient1 ingredient2 ingredient3 cocktail1 cocktail2 cocktail3
           left-hand right-hand
           on-table
           empty clean contains-ingredient1 contains-ingredient2 contains-ingredient3 contains-cocktail1 contains-cocktail2 contains-cocktail3
  )
  (:init
    (and (on-table shaker1) (empty shaker1) (clean shaker1)
         (on-table shotglass1) (empty shotglass1) (clean shotglass1)
         (on-table shotglass2) (empty shotglass2) (clean shotglass2)
         (on-table shotglass3) (empty shotglass3) (clean shotglass3)
         (holding left-hand) (holding right-hand)
         (not (contains-beverage shaker1))
         (not (contains-cocktail1 shotglass1))
         (not (contains-cocktail2 shotglass2))
         (not (contains-cocktail3 shotglass3))
    )
    (and (contains-ingredient1 shaker1) (contains-ingredient3 shaker1))
    (and (contains-ingredient2 shaker1) (contains-ingredient3 shaker1))
    (and (contains-ingredient1 shaker1) (contains-ingredient2 shaker1))
    (and (contains-ingredient1 shotglass1) (empty shotglass2) (empty shotglass3))
    (and (empty shotglass1) (contains-ingredient3 shotglass1))
    (and (empty shotglass2) (contains-ingredient2 shotglass2))
    (and (empty shotglass3) (contains-ingredient1 shotglass3))
  )
  (:goal (and (contains-cocktail1 shotglass1) (contains-cocktail3 shotglass2) (contains-cocktail2 shotglass3)))
)