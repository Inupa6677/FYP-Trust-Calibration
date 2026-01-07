(define (problem storage-3)
(:domain Storage-Propositional)
(:objects
	depot48-1-1 depot48-1-2 depot48-1-3 container-0-0 - storearea
	hoist0 hoist2 hoist1 - hoist
	crate0 - crate
	container0 - container
	depot48 - depot
	loadarea - transitarea)

(:init
	(connected depot48-1-1 depot48-1-2)
	(connected depot48-1-2 depot48-1-3)
	(in depot48-1-1 depot48)
	(in depot48-1-2 depot48)
	(in depot48-1-3 depot48)
	(on crate0 container-0-0)
	(in crate0 container0)
	(connected loadarea container-0-0)
	(connected loadarea depot48-1-2)
	(at hoist0 depot48-1-2)
	(available hoist0)
	(at hoist2 depot48-1-1)
	(available hoist2)
	(at hoist1 depot48-1-3)
	(available hoist1))

(:goal (and
	(in crate0 depot48)
	(clear container-0-0))))