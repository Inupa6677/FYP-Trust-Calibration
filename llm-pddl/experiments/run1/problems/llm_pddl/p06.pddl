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
    (contains-cocktail4 ?shotglass)
  )

  (:action grasp-container
    :parameters (?container)
    :precondition (and (on-table ?container) (not (and (holding ?container) (not (empty ?container)))))
    :effect (and (holding ?container) (not (on-table ?container)) (not (empty ?container)) (not (clean ?container)))
  )

  (:action leave-container
    :parameters (?container)
    :precondition (and (holding ?container))
    :effect (and (on-table ?container) (not (holding ?container)) (empty ?container) (clean ?container))
  )

  (:action fill-shotglass-with-ingredient1
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient1 ?shotglass)))
    :effect (and (contains-ingredient1 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient2
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient2 ?shotglass)))
    :effect (and (contains-ingredient2 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action fill-shotglass-with-ingredient3
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (clean ?shotglass) (not (contains-ingredient3 ?shotglass)))
    :effect (and (contains-ingredient3 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action refill-shotglass-with-ingredient1
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (contains-ingredient1 ?dispenser) (not (contains-ingredient1 ?shotglass)))
    :effect (and (contains-ingredient1 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action refill-shotglass-with-ingredient2
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (contains-ingredient2 ?dispenser) (not (contains-ingredient2 ?shotglass)))
    :effect (and (contains-ingredient2 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action refill-shotglass-with-ingredient3
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (contains-ingredient3 ?dispenser) (not (contains-ingredient3 ?shotglass)))
    :effect (and (contains-ingredient3 ?shotglass) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )

  (:action empty-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (contains-beverage ?shotglass))
    :effect (and (empty ?shotglass) (not (contains-beverage ?shotglass)))
  )

  (:action clean-shotglass
    :parameters (?shotglass)
    :precondition (and (holding ?shotglass) (empty ?shotglass) (not (contains-beverage ?shotglass)) (empty-hand))
    :effect (and (clean ?shotglass) (not (empty ?shotglass)))
  )

  (:action pour-ingredient1-to-shaker
    :parameters (?shotglass ?shaker)
    :precondition (and (holding ?shotglass) (contains-ingredient1 ?shotglass) (empty ?shaker))
    :effect (and (contains-ingredient1 ?shaker) (not (contains-ingredient1 ?shotglass)) (not (empty ?shaker)))
  )

  (:action pour-ingredient2-to-shaker
    :parameters (?shotglass ?shaker)
    :precondition (and (holding ?shotglass) (contains-ingredient2 ?shotglass) (empty ?shaker))
    :effect (and (contains-ingredient2 ?shaker) (not (contains-ingredient2 ?shotglass)) (not (empty ?shaker)))
  )

  (:action pour-ingredient3-to-shaker
    :parameters (?shotglass ?shaker)
    :precondition (and (holding ?shotglass) (contains-ingredient3 ?shotglass) (empty ?shaker))
    :effect (and (contains-ingredient3 ?shaker) (not (contains-ingredient3 ?shotglass)) (not (empty ?shaker)))
  )

  (:action empty-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (contains-beverage ?shaker))
    :effect (and (empty ?shaker) (not (contains-beverage ?shaker)))
  )

  (:action clean-shaker
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty ?shaker) (empty-hand))
    :effect (and (clean ?shaker) (not (empty ?shaker)))
  )

  (:action shake-cocktail
    :parameters (?shaker)
    :precondition (and (holding ?shaker) (empty-hand) (contains-ingredient1 ?shaker) (contains-ingredient2 ?shaker))
    :effect (and (contains-cocktail1 ?shaker) (not (contains-ingredient1 ?shaker)) (not (contains-ingredient2 ?shaker)))
  )

  (:action pour-cocktail-to-shotglass
    :parameters (?shaker ?shotglass)
    :precondition (and (holding ?shaker) (contains-cocktail1 ?shaker) (shaked ?shaker) (empty ?shotglass) (clean ?shotglass))
    :effect (and (contains-cocktail1 ?shotglass) (not (contains-cocktail1 ?shaker)) (not (shaked ?shaker)) (not (empty ?shotglass)) (not (clean ?shotglass)))
  )
)

(define (problem RobotBarman-Problem)
  (:domain RobotBarman)
  (:objects shaker1 dispenser1 dispenser2 dispenser3 shotglass1 shotglass2 shotglass3 shotglass4 shotglass5 - Container
           cocktail1 cocktail2 cocktail3 cocktail4 - Beverage
           ingredient1 ingredient2 ingredient3 - Ingredient)
  (:init
    (and (on-table shaker1) (empty shaker1) (clean shaker1) (empty-hand)
         (on-table dispenser1) (contains-ingredient1 dispenser1) (contains-ingredient2 dispenser2) (contains-ingredient3 dispenser3)
         (on-table shotglass1) (on-table shotglass2) (on-table shotglass3) (on-table shotglass4) (on-table shotglass5)
         (empty shotglass1) (empty shotglass2) (empty shotglass3) (empty shotglass4) (empty shotglass5)
         (clean shotglass1) (clean shotglass2) (clean shotglass3) (clean shotglass4) (clean shotglass5))
    (contains-cocktail2 shotglass1)
    (contains-cocktail3 shotglass2)
    (contains-cocktail1 shotglass3)
    (contains-cocktail4 shotglass4)
  )
  (:goal (and (contains-cocktail1 shotglass3) (contains-cocktail2 shotglass1) (contains-cocktail3 shotglass2) (contains-cocktail4 shotglass4)))
)