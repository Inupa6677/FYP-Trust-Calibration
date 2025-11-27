(define (problem storage-10)
(:domain Storage-Propositional)
(:objects
	depot48-1-1 depot48-1-2 depot48-2-1 depot48-2-2 - storearea
	hoist0 hoist1 - hoist
	crate0 crate1 - crate
	container0 - container
	depot48 - depot
	loadarea - transitarea)

(:init
	(connected depot48-1-1 depot48-1-2)
	(connected depot48-1-2 depot48-2-1)
	(connected depot48-1-2 depot48-2-2)
	(in depot48-1-1 depot48)
	(in depot48-1-2 depot48)
	(in depot48-2-1 depot48)
	(in depot48-2-2 depot48)
	(on crate0 container-0-0)
	(on crate1 container-0-1)
	(in crate0 container0)
	(in crate1 container0)
	(in container-0-0 container0)
	(in container-0-1 container0)
	(connected loadarea container-0-0) 
	(connected container-0-0 loadarea)
	(connected loadarea container-0-1) 
	(connected container-0-1 loadarea)
	(at hoist0 depot48-1-2)
	(available hoist0)
	(at hoist1 depot48-1-1)
	(available hoist1))

(:goal (and
	(in crate0 depot48)
	(in crate1 depot48))))