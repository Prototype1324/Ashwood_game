scenes = {
    "coffee_shop": {
        "name": "Blackwood Coffee House",
        "objective": "Investigate the disappearances in Ashwood.",
        "key_info": "The enigmatic owner, Mr. Blackwood, and the strange happenings in the shop.",
        "start_screen": "opening",
        "screens": {
            "opening": {
                "text": (
                    "It's the year 1951. You are Sam Carter, a former Catholic priest and the best investigator in New York, "
                    "known for solving the unsolvable—and the supernatural.\n"
                    "You've been sent to the isolated town of Ashwood to investigate a string of bizarre missing persons reports. "
                    "All the victims were last seen at a peculiar coffee shop on the edge of town.\n"
                    "The townsfolk whisper about the owner, Mr. Blackwood, but no one dares speak openly.\n"
                    "You sense something lurking beneath the surface of this case."
                ),
                "options": [
                    "Click to continue"
                ],
                "next": ["intro"]
            },

            "intro": {
                "text": (
                    "A cold mist clings to the empty streets as you approach the Blackwood Coffee House. "
                    "The sign above the door flickers and creaks in the wind. "
                    "The windows are fogged, hiding whatever lies within.\n\n"
                    "You step inside. The air is thick with the scent of coffee and something else—something metallic.\n\n"
                    "Mr. Blackwood stands behind the counter, watching you with a thin smile."
                ),
                "options": [
                    "Approach Mr. Blackwood",
                    "Look around",
                    "Sit and observe",
                    "Leave"
                ],
                "next": ["kitchen_door", "search_room", "sit_observe", "leave_shop"]
            },

            # --- Coffee Cup Path ---
            "coffee_cup": {
                "text": (
                    "A lone cup of coffee sits on a table, still steaming as if waiting for someone. "
                    "The smell is off—beneath the aroma of beans, there’s the sharp tang of blood. "
                    "Floating on the surface is a small silver locket."
                ),
                "options": [
                    "Take locket",
                    "Examine cup",
                    "Leave it",
                    "Look around"
                ],
                "next": ["take_locket", "examine_cup", "leave_cup", "observe_room"]
            },
            "take_locket": {
                "text": (
                    "You pocket the locket. Inside is a photo of a young woman—the same woman reported missing last week. "
                    "The room seems to grow colder the moment you touch it."
                ),
                "options": [
                    "Back to room",
                    "To kitchen",
                    "Ask Blackwood",
                    "Leave"
                ],
                "next": ["search_room", "kitchen_door", "question_blackwood", "leave_shop"]
            },
            "examine_cup": {
                "text": (
                    "The cup is ordinary, but the liquid is thick, darker than coffee should be. "
                    "Your trained eye catches faint fingerprints burned into the porcelain, as if scorched there."
                ),
                "options": [
                    "Take locket",
                    "Back to room",
                    "To kitchen",
                    "Leave"
                ],
                "next": ["take_locket", "search_room", "kitchen_door", "leave_shop"]
            },
            "leave_cup": {
                "text": (
                    "You decide not to touch the cup. "
                    "Still, it feels as if unseen eyes are disappointed with your choice."
                ),
                "options": [
                    "Search room",
                    "To kitchen",
                    "Call out",
                    "Leave"
                ],
                "next": ["search_room", "kitchen_door", "call_out", "leave_shop"]
            },

            # --- Kitchen Path ---
            "kitchen_door": {
                "text": (
                    "The kitchen door creaks open. A tall man in a stained apron stirs a pot without turning to face you.\n"
                    "His voice is smooth and deliberate: 'Welcome, Detective Carter. I was wondering when you'd arrive.'"
                ),
                "options": [
                    "Demand answers",
                    "Observe",
                    "Inspect pot",
                    "Back to room"
                ],
                "next": ["demand_name", "observe_blackwood", "inspect_pot", "search_room"]
            },
            "demand_name": {
                "text": (
                    "The man chuckles. 'Names have power, Detective. But you already know mine: Blackwood.'\n"
                    "He finally turns, eyes gleaming unnaturally."
                ),
                "options": [
                    "Ask about missing",
                    "Step back",
                    "Use crucifix",
                    "Inspect pot"
                ],
                "next": ["missing_people", "search_room", "use_crucifix", "inspect_pot"]
            },
            "observe_blackwood": {
                "text": (
                    "He continues stirring, as if performing a ritual. Symbols are carved into the wood of the spoon, glowing faintly."
                ),
                "options": [
                    "Confront",
                    "Inspect pot",
                    "Back to room",
                    "Use crucifix"
                ],
                "next": ["demand_name", "inspect_pot", "search_room", "use_crucifix"]
            },
            "inspect_pot": {
                "text": (
                    "You peer into the pot. It isn’t stew—it’s thick, red, and swirling with symbols. "
                    "The surface shifts, forming a screaming face before sinking back."
                ),
                "options": [
                    "Recoil",
                    "Accuse Blackwood",
                    "Use crucifix",
                    "Flee"
                ],
                "next": ["search_room", "missing_people", "use_crucifix", "leave_shop"]
            },

            # --- Room Search Path ---
            "search_room": {
                "text": (
                    "You scan the coffee shop. Footprints lead into the shadows. "
                    "Behind the counter, you spot a leather ledger filled with names—many of them crossed out. "
                    "The record player skips endlessly on a single warped note."
                ),
                "options": [
                    "Take ledger",
                    "Follow footprints",
                    "Inspect record",
                    "To kitchen"
                ],
                "next": ["take_ledger", "follow_footprints", "inspect_record", "kitchen_door"]
            },
            "take_ledger": {
                "text": (
                    "You slip the ledger into your coat. The names match the list of missing persons. "
                    "The book pulses faintly, almost alive."
                ),
                "options": [
                    "To kitchen",
                    "Inspect record",
                    "Follow footprints",
                    "Leave"
                ],
                "next": ["kitchen_door", "inspect_record", "follow_footprints", "leave_shop"]
            },
            "follow_footprints": {
                "text": (
                    "The footprints end at a wall. On closer inspection, there’s a hidden door. "
                    "Behind it, stairs descend into darkness."
                ),
                "options": [
                    "Enter stairs",
                    "Back to counter",
                    "Call Blackwood",
                    "Leave"
                ],
                "next": ["hidden_stairs", "search_room", "missing_people", "leave_shop"]
            },
            "inspect_record": {
                "text": (
                    "The record player scratches endlessly. "
                    "Lifting the record, you find a human tooth embedded beneath the needle."
                ),
                "options": [
                    "Take tooth",
                    "Smash record",
                    "Back to counter",
                    "Leave"
                ],
                "next": ["tooth_evidence", "search_room", "search_room", "leave_shop"]
            },
            "tooth_evidence": {
                "text": (
                    "You pocket the tooth. The music stops, but the silence is heavier than before."
                ),
                "options": [
                    "To kitchen",
                    "Inspect counter",
                    "Follow footprints",
                    "Leave"
                ],
                "next": ["kitchen_door", "search_room", "follow_footprints", "leave_shop"]
            },

            # --- Hidden Stairs Path ---
            "hidden_stairs": {
                "text": (
                    "The stairs groan under your weight. At the bottom is a cellar lit by candlelight. "
                    "Chains line the walls. In the center is a circle of ash and blood. "
                    "You feel something ancient stirring."
                ),
                "options": [
                    "Step in circle",
                    "Use crucifix",
                    "Upstairs",
                    "Wait"
                ],
                "next": ["bad_end", "good_end", "search_room", "wait_circle"]
            },
            "wait_circle": {
                "text": (
                    "You wait. The candles flicker, and shadows twist into faces. "
                    "You realize the victims are trapped here, screaming silently from the dark."
                ),
                "options": [
                    "Step in circle",
                    "Use crucifix",
                    "Upstairs",
                    "Pray"
                ],
                "next": ["bad_end", "good_end", "search_room", "good_end"]
            },

            # --- Calling on Priest Training ---
            "use_crucifix": {
                "text": (
                    "You clutch your crucifix and begin reciting a prayer. "
                    "Blackwood snarls, his form flickering like smoke. "
                    "'You cannot banish what you don’t understand, priest!'"
                ),
                "options": [
                    "Pray harder",
                    "Step back",
                    "Accuse him",
                    "Run"
                ],
                "next": ["good_end", "search_room", "missing_people", "leave_shop"]
            },

            # --- Call Out Path ---
            "call_out": {
                "text": (
                    "Your voice echoes through the empty shop. The lamps flicker, and a chair scrapes across the floor by itself. "
                    "From the shadows, a pale man in a black suit steps forward. His smile is thin, and his eyes glint unnaturally.\n\n"
                    "Mr. Blackwood: 'Detective Carter... I was wondering when you would arrive.'"
                ),
                "options": [
                    "Ask about missing",
                    "Observe",
                    "Use crucifix",
                    "Retreat"
                ],
                "next": ["missing_people", "observe_blackwood", "use_crucifix", "leave_shop"]
            },

            # --- Blackwood Dialog ---
            "missing_people": {
                "text": (
                    "Blackwood smirks. 'People come and go, Detective. Some simply don’t wish to be found.' "
                    "His eyes glow faintly in the dim light."
                ),
                "options": [
                    "Press him",
                    "Use crucifix",
                    "Back away",
                    "Flee"
                ],
                "next": ["demand_name", "use_crucifix", "search_room", "leave_shop"]
            },

            # --- Endings ---
            "good_end": {
                "text": (
                    "Your prayer resonates through the room. "
                    "The circle in the cellar burns with holy light, releasing the trapped souls. "
                    "Blackwood screams as his body crumbles into ash.\n\n"
                    "The townsfolk will be free of his curse.\n"
                    "Case closed."
                ),
                "options": ["Restart", "", "", ""],
                "next": ["opening", "", "", ""]
            },
            "bad_end": {
                "text": (
                    "The moment you step into the circle, the candles flare. "
                    "Chains wrap around your body, dragging you down into the blood-soaked floor. "
                    "You realize too late that you’ve taken the place of the missing.\n\n"
                    "Ashwood will never escape Blackwood’s grasp."
                ),
                "options": ["Restart", "", "", ""],
                "next": ["opening", "", "", ""]
            },
            "leave_shop": {
                "text": (
                    "You step outside. The mist is thicker now. "
                    "Every road you walk leads you back to the coffee shop. "
                    "The curse won’t let you go."
                ),
                "options": ["Restart", "", "", ""],
                "next": ["opening", "", "", ""]
            }
        }
    }
}
