MOCK_FLIGHT = {
    "tokyo": [
        {
            "id":"FL001",
            "airline": "Japan Airlines",
            "flight_number":"JL005",
            "departure_city": "Los Angeles",
            "arrival_city": "Tpkyo Narita",
            "departure_time": "11:30",
            "arrival_time": "15:30+1",
            "duration": "12h 00m",
            "stops":0,
            "class": "Economy",
            "price": 850,
            "currency": "USD"
        }
        {...},
        {...},
        {...}
    ]
    "paris":[
        {...},
        {...},
        {...}
    ]
}



MOCK_HOTEL = {
    "tokyo":[
        {
            "id": "HT001",
            "name": "Park Hyatt Tokyo",
            "neighbourhood":"Shinjuku",
            "rating": 4.8,
            "reviews": 2847,
            "price_per_night": 450,
            "currency": "USD",
            "amenities":["spa", "pool", "Gym", "Restaurant", "Bar","Room Service"],
            "description":"Luxury hotel featured in 'Lost in Translation'. Stunning views of Mt. Fuji and Tokyo skyline",
            "traveler_type":["couples","luxury","business"]

        },
        {...},
        {...},
        {...},
        {...},
    ],
    "paris":[
        {...},
        {...},
        {...},

    ]
}

MOCK_ACTIVITIES = {
    "tokyo":[
        #cultural activities
        {
            "id":"AC001",
            "name":"Senso-ji Temple & Asakusa Walking Tour",
            "category": "Culture",
            "duration":"3 hours",
            "price": 45,
            "currency": "USD",
            "rating": 4.7,
            "description":" Explore Tokyo's oldest temple and the traditional Asakusa district with a local guide.",
            "best_for": ["culture","history","photography"],
            "location": "Asakusa"
        },
        {...},
        {...},
        {...},
        # food activities
        {...},
        {...},
        #Entertainment Activities
        {...},
        {...},
        {...},
        {...},
        {...},
        # Nature and View
        {...},
        {...},
        {...},
        {...},
    ],
    "paris":[...]
}

MOCK_RESTAURANTS = {
    "tokyo":[
        {

        "id":"RS001",
        "name": "Sukiyabashi Jiro",
        "cuisine": "Sushi",
        "price_range": "$$$$$",
        "rating": 4.9,
        "neighbourhood":"Ginza",
        "description":" Lengendary 3-Michelin star sushi. Reservation required months in advance",
        "best_for":["special occasion","sushi lovers"]
        },
        {...},
        {...},
        {...},
    ],
    "paris":[...]
}