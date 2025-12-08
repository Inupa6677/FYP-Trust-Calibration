(define (problem storage-10)
(:domain Storage-Propositional)
(:objects
	depot48-1-1 depot48-1-2 depot48-1-3 - storearea
	hoist0 hoist1 hoist2 - hoist
	crate0 crate1 - crate
	container0 - container
	depot48 - depot
	loadarea - transitarea)

(:init
	(connected depot48-1-1 depot48-1-2)
	(connected depot48-1-2 depot48-1-3)
	(in depot48-1-1 depot48)
	(in depot48-1-2 depot48)
	(in depot48-1-3 depot48)
	(on crate0 container0)
	(on crate1 container0)
	(in crate0 container0)
	(in crate1 container0)
	(connected loadarea container0) 
	(connected container0 loadarea)
	(at hoist0 depot48-1-2)
	(available hoist0)
	(at hoist1 depot48-1-1)
	(available hoist1)
	(at hoist2 depot48-1-3)
	(available hoist2))

(:goal (and
	(in crate0 depot48)
	(in crate1 depot48))))