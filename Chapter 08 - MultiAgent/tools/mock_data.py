MOCK_FLIGHT = {
    "tokyo": [
        {
            "id":"FL001",
            "airline": "Japan Airlines",
            "flight_number":"JL005",
            "departure_city": "Los Angeles",
            "arrival_city": "Tokyo Narita",
            "departure_time": "11:30",
            "arrival_time": "15:30+1",
            "duration": "12h 00m",
            "stops": 0,
            "class": "Economy",
            "price": 850,
            "currency": "USD"
        },
        {
            "id":"FL002",
            "airline": "All Nippon Airways",
            "flight_number":"NH107",
            "departure_city": "New York",
            "arrival_city": "Tokyo Haneda",
            "departure_time": "13:45",
            "arrival_time": "18:00+1",
            "duration": "13h 15m",
            "stops": 0,
            "class": "Business",
            "price": 2200,
            "currency": "USD"
        },
        {
            "id":"FL003",
            "airline": "Delta Airlines",
            "flight_number":"DL275",
            "departure_city": "San Francisco",
            "arrival_city": "Tokyo Narita",
            "departure_time": "09:00",
            "arrival_time": "13:30+1",
            "duration": "11h 30m",
            "stops": 1,
            "class": "Economy",
            "price": 780,
            "currency": "USD"
        }
    ],
    "paris": [
        {
            "id":"FL101",
            "airline": "Air France",
            "flight_number":"AF007",
            "departure_city": "New York",
            "arrival_city": "Paris Charles de Gaulle",
            "departure_time": "18:00",
            "arrival_time": "07:30+1",
            "duration": "7h 30m",
            "stops": 0,
            "class": "Economy",
            "price": 650,
            "currency": "USD"
        },
        {
            "id":"FL102",
            "airline": "British Airways",
            "flight_number":"BA304",
            "departure_city": "London",
            "arrival_city": "Paris Charles de Gaulle",
            "departure_time": "07:15",
            "arrival_time": "09:30",
            "duration": "1h 15m",
            "stops": 0,
            "class": "Economy",
            "price": 120,
            "currency": "USD"
        },
        {
            "id":"FL103",
            "airline": "Lufthansa",
            "flight_number":"LH123",
            "departure_city": "Frankfurt",
            "arrival_city": "Paris Charles de Gaulle",
            "departure_time": "12:20",
            "arrival_time": "13:50",
            "duration": "1h 30m",
            "stops": 0,
            "class": "Business",
            "price": 450,
            "currency": "USD"
        }
    ]
}



MOCK_HOTEL = {
    "tokyo": [
        {
            "id": "HT001",
            "name": "Park Hyatt Tokyo",
            "neighborhood": "Shinjuku",
            "rating": 4.8,
            "reviews": 2847,
            "price_per_night": 450,
            "currency": "USD",
            "amenities": ["spa", "pool", "gym", "restaurant", "bar", "room service"],
            "description": "Luxury hotel featured in 'Lost in Translation'. Stunning views of Mt. Fuji and Tokyo skyline",
            "traveler_type": ["couples", "luxury", "business"]
        },
        {
            "id": "HT002",
            "name": "The Ritz-Carlton Tokyo",
            "neighborhood": "Roppongi",
            "rating": 4.7,
            "reviews": 1985,
            "price_per_night": 520,
            "currency": "USD",
            "amenities": ["spa", "pool", "gym", "restaurant", "bar", "conference room"],
            "description": "Upscale hotel with panoramic city views, Michelin-star dining, and premium service.",
            "traveler_type": ["luxury", "business", "couples"]
        },
        {
            "id": "HT003",
            "name": "Shinjuku Granbell Hotel",
            "neighborhood": "Shinjuku",
            "rating": 4.2,
            "reviews": 1123,
            "price_per_night": 120,
            "currency": "USD",
            "amenities": ["gym", "restaurant", "bar", "rooftop terrace"],
            "description": "Modern boutique hotel in the heart of Shinjuku with stylish rooms and rooftop views.",
            "traveler_type": ["solo", "couples", "budget"]
        },
        {
            "id": "HT004",
            "name": "Hotel Niwa Tokyo",
            "neighborhood": "Chiyoda",
            "rating": 4.5,
            "reviews": 1540,
            "price_per_night": 200,
            "currency": "USD",
            "amenities": ["gym", "restaurant", "tea lounge", "garden"],
            "description": "Charming hotel with traditional Japanese decor and tranquil garden spaces.",
            "traveler_type": ["business", "couples", "solo"]
        },
        {
            "id": "HT005",
            "name": "Mitsui Garden Hotel Ginza Premier",
            "neighborhood": "Ginza",
            "rating": 4.3,
            "reviews": 980,
            "price_per_night": 250,
            "currency": "USD",
            "amenities": ["gym", "restaurant", "bar", "lounge"],
            "description": "Stylish hotel with rooftop views in the upscale Ginza district, close to shopping and nightlife.",
            "traveler_type": ["luxury", "business", "couples"]
        }
    ],
    "paris": [
        {
            "id": "HT101",
            "name": "Le Meurice",
            "neighborhood": "1st arrondissement",
            "rating": 4.9,
            "reviews": 1782,
            "price_per_night": 600,
            "currency": "USD",
            "amenities": ["spa", "restaurant", "bar", "gym", "room service"],
            "description": "Historic luxury palace hotel with opulent interiors and Michelin-star dining.",
            "traveler_type": ["luxury", "couples", "business"]
        },
        {
            "id": "HT102",
            "name": "Hôtel Plaza Athénée",
            "neighborhood": "8th arrondissement",
            "rating": 4.8,
            "reviews": 1650,
            "price_per_night": 580,
            "currency": "USD",
            "amenities": ["spa", "restaurant", "bar", "gym", "rooftop terrace"],
            "description": "Iconic Parisian hotel offering luxury rooms, designer decor, and Eiffel Tower views.",
            "traveler_type": ["luxury", "romantic", "business"]
        },
        {
            "id": "HT103",
            "name": "Hotel Le Bellechasse",
            "neighborhood": "7th arrondissement",
            "rating": 4.4,
            "reviews": 845,
            "price_per_night": 220,
            "currency": "USD",
            "amenities": ["restaurant", "bar", "art gallery", "lounge"],
            "description": "Boutique hotel with artistic design and a cozy atmosphere, close to major landmarks.",
            "traveler_type": ["couples", "solo", "budget"]
        },
        {
            "id": "HT104",
            "name": "Novotel Paris Les Halles",
            "neighborhood": "1st arrondissement",
            "rating": 4.2,
            "reviews": 1340,
            "price_per_night": 180,
            "currency": "USD",
            "amenities": ["gym", "restaurant", "bar", "family friendly"],
            "description": "Modern hotel in central Paris, ideal for families and business travelers.",
            "traveler_type": ["family", "business", "couples"]
        },
        {
            "id": "HT105",
            "name": "CitizenM Paris Gare de Lyon",
            "neighborhood": "12th arrondissement",
            "rating": 4.3,
            "reviews": 910,
            "price_per_night": 150,
            "currency": "USD",
            "amenities": ["bar", "lounge", "self check-in", "wifi"],
            "description": "Trendy hotel with smart rooms and modern tech for a connected stay.",
            "traveler_type": ["solo", "business", "budget"]
        }
    ]
}



MOCK_ACTIVITIES = {
    "tokyo": [
        # Culture
        {
            "id":"AC001",
            "name":"Senso-ji Temple & Asakusa Walking Tour",
            "category": "Culture",
            "duration":"3 hours",
            "price": 45,
            "currency": "USD",
            "rating": 4.7,
            "description":"Explore Tokyo's oldest temple and the traditional Asakusa district with a local guide.",
            "best_for": ["culture","history","photography"],
            "location": "Asakusa"
        },
        {
            "id":"AC002",
            "name":"Tokyo National Museum Visit",
            "category": "Culture",
            "duration":"2 hours",
            "price": 20,
            "currency": "USD",
            "rating": 4.6,
            "description":"Discover Japanese art, samurai armor, and historic artifacts at the country's oldest museum.",
            "best_for": ["culture","history","learning"],
            "location": "Ueno"
        },
        {
            "id":"AC003",
            "name":"Kabuki Theater Show",
            "category": "Culture",
            "duration":"2.5 hours",
            "price": 75,
            "currency": "USD",
            "rating": 4.8,
            "description":"Experience traditional Japanese performing arts in a historic theater.",
            "best_for": ["culture","theater","performance"],
            "location": "Ginza"
        },
        # Food
        {
            "id":"AC004",
            "name":"Tsukiji Fish Market Sushi Tour",
            "category": "Food",
            "duration":"3 hours",
            "price": 60,
            "currency": "USD",
            "rating": 4.9,
            "description":"Taste fresh sushi and learn from local chefs at Tokyo’s famous fish market.",
            "best_for": ["food","culture","culinary"],
            "location": "Tsukiji"
        },
        {
            "id":"AC005",
            "name":"Ramen Making Workshop",
            "category": "Food",
            "duration":"2 hours",
            "price": 50,
            "currency": "USD",
            "rating": 4.8,
            "description":"Hands-on experience making authentic Japanese ramen from scratch.",
            "best_for": ["food","cooking","family"],
            "location": "Shinjuku"
        },
        # Entertainment
        {
            "id":"AC006",
            "name":"Tokyo Disneyland",
            "category": "Entertainment",
            "duration":"Full Day",
            "price": 85,
            "currency": "USD",
            "rating": 4.7,
            "description":"Enjoy rides, parades, and shows at Tokyo's iconic theme park.",
            "best_for": ["family","fun","adventure"],
            "location": "Urayasu"
        },
        {
            "id":"AC007",
            "name":"Robot Restaurant Show",
            "category": "Entertainment",
            "duration":"2 hours",
            "price": 60,
            "currency": "USD",
            "rating": 4.5,
            "description":"Watch a futuristic robot performance combined with music, lights, and dance.",
            "best_for": ["fun","unique","nightlife"],
            "location": "Shinjuku"
        },
        {
            "id":"AC008",
            "name":"VR Zone Shinjuku",
            "category": "Entertainment",
            "duration":"2 hours",
            "price": 40,
            "currency": "USD",
            "rating": 4.4,
            "description":"Immersive virtual reality games and experiences in a high-tech gaming center.",
            "best_for": ["technology","games","adventure"],
            "location": "Shinjuku"
        },
        # Nature & View
        {
            "id":"AC009",
            "name":"Mount Takao Hiking Tour",
            "category": "Nature and View",
            "duration":"5 hours",
            "price": 30,
            "currency": "USD",
            "rating": 4.8,
            "description":"Scenic hike with temples, wildlife, and panoramic views of Tokyo and Mt. Fuji.",
            "best_for": ["nature","hiking","photography"],
            "location": "Hachioji"
        },
        {
            "id":"AC010",
            "name":"Odaiba Seaside Park & Statue of Liberty Replica",
            "category": "Nature and View",
            "duration":"3 hours",
            "price": 15,
            "currency": "USD",
            "rating": 4.6,
            "description":"Relax at Odaiba beach and enjoy views of Tokyo Bay and city skyline.",
            "best_for": ["nature","relaxation","photography"],
            "location": "Odaiba"
        },
        {
            "id":"AC011",
            "name":"Shinjuku Gyoen National Garden",
            "category": "Nature and View",
            "duration":"2 hours",
            "price": 10,
            "currency": "USD",
            "rating": 4.7,
            "description":"Peaceful stroll through beautifully landscaped gardens blending traditional Japanese, English, and French styles.",
            "best_for": ["nature","relaxation","photography"],
            "location": "Shinjuku"
        }
    ],
    "paris": [
        # Culture
        {
            "id":"AC101",
            "name":"Louvre Museum Guided Tour",
            "category": "Culture",
            "duration":"3 hours",
            "price": 60,
            "currency": "USD",
            "rating": 4.9,
            "description":"Explore the world’s largest art museum and see iconic works like the Mona Lisa.",
            "best_for": ["culture","art","history"],
            "location": "1st arrondissement"
        },
        {
            "id":"AC102",
            "name":"Montmartre & Sacré-Cœur Walking Tour",
            "category": "Culture",
            "duration":"2.5 hours",
            "price": 35,
            "currency": "USD",
            "rating": 4.7,
            "description":"Discover the artistic history and stunning views of Paris from Montmartre hill.",
            "best_for": ["culture","photography","walking"],
            "location": "Montmartre"
        },
        # Food
        {
            "id":"AC103",
            "name":"Paris Pastry & Chocolate Tasting Tour",
            "category": "Food",
            "duration":"3 hours",
            "price": 50,
            "currency": "USD",
            "rating": 4.8,
            "description":"Sample pastries, chocolates, and French delicacies in the heart of Paris.",
            "best_for": ["food","culinary","couples"],
            "location": "1st arrondissement"
        },
        {
            "id":"AC104",
            "name":"French Cooking Class",
            "category": "Food",
            "duration":"3 hours",
            "price": 75,
            "currency": "USD",
            "rating": 4.9,
            "description":"Learn to cook classic French dishes with a local chef.",
            "best_for": ["food","cooking","family"],
            "location": "Marais"
        },
        # Entertainment
        {
            "id":"AC105",
            "name":"Moulin Rouge Cabaret Show",
            "category": "Entertainment",
            "duration":"2 hours",
            "price": 120,
            "currency": "USD",
            "rating": 4.7,
            "description":"Experience a legendary Parisian cabaret show with music, dance, and costumes.",
            "best_for": ["nightlife","culture","fun"],
            "location": "Montmartre"
        },
        {
            "id":"AC106",
            "name":"Seine River Cruise",
            "category": "Entertainment",
            "duration":"1.5 hours",
            "price": 35,
            "currency": "USD",
            "rating": 4.6,
            "description":"Scenic boat cruise along the Seine with views of Paris landmarks.",
            "best_for": ["relaxation","photography","family"],
            "location": "Seine River"
        },
        # Nature & View
        {
            "id":"AC107",
            "name":"Eiffel Tower Visit & Summit Access",
            "category": "Nature and View",
            "duration":"2 hours",
            "price": 50,
            "currency": "USD",
            "rating": 4.9,
            "description":"Ascend the Eiffel Tower and enjoy breathtaking panoramic views of Paris.",
            "best_for": ["photography","sightseeing","romantic"],
            "location": "7th arrondissement"
        },
        {
            "id":"AC108",
            "name":"Luxembourg Gardens Stroll",
            "category": "Nature and View",
            "duration":"2 hours",
            "price": 0,
            "currency": "USD",
            "rating": 4.8,
            "description":"Relax and enjoy beautifully manicured gardens in the heart of Paris.",
            "best_for": ["nature","relaxation","family"],
            "location": "6th arrondissement"
        }
    ]
}


MOCK_RESTAURANTS = {
    "tokyo": [
        {
            "id":"RS001",
            "name": "Sukiyabashi Jiro",
            "cuisine": "Sushi",
            "price_range": "$$$$$",
            "rating": 4.9,
            "neighborhood":"Ginza",
            "description":"Legendary 3-Michelin star sushi. Reservation required months in advance.",
            "best_for":["special occasion","sushi lovers"]
        },
        {
            "id":"RS002",
            "name": "Ichiran Ramen Shibuya",
            "cuisine": "Ramen",
            "price_range": "$$",
            "rating": 4.7,
            "neighborhood":"Shibuya",
            "description":"Famous tonkotsu ramen with solo dining booths for focused enjoyment.",
            "best_for":["ramen lovers","casual","solo dining"]
        },
        {
            "id":"RS003",
            "name": "Narisawa",
            "cuisine": "Japanese Contemporary",
            "price_range": "$$$$$",
            "rating": 4.8,
            "neighborhood":"Minato",
            "description":"Innovative, Michelin 2-star Japanese cuisine emphasizing natural ingredients and seasonal menus.",
            "best_for":["gourmet","special occasion","foodies"]
        },
        {
            "id":"RS004",
            "name": "Tsunahachi Tempura",
            "cuisine": "Tempura",
            "price_range": "$$$",
            "rating": 4.5,
            "neighborhood":"Shinjuku",
            "description":"Traditional tempura served in an elegant setting with fresh seafood.",
            "best_for":["family","traditional cuisine","casual"]
        }
    ],
    "paris": [
        {
            "id":"RS101",
            "name": "Le Jules Verne",
            "cuisine": "French Fine Dining",
            "price_range": "$$$$$",
            "rating": 4.9,
            "neighborhood":"7th arrondissement",
            "description":"Michelin-star restaurant located inside the Eiffel Tower offering stunning views.",
            "best_for":["romantic","special occasion","fine dining"]
        },
        {
            "id":"RS102",
            "name": "L'As du Fallafel",
            "cuisine": "Middle Eastern",
            "price_range": "$",
            "rating": 4.7,
            "neighborhood":"Marais",
            "description":"Legendary falafel sandwiches in the bustling Jewish quarter.",
            "best_for":["casual","street food","budget"]
        },
        {
            "id":"RS103",
            "name": "Le Comptoir du Relais",
            "cuisine": "French Bistro",
            "price_range": "$$$",
            "rating": 4.6,
            "neighborhood":"6th arrondissement",
            "description":"Classic French bistro with seasonal dishes and a cozy atmosphere.",
            "best_for":["bistro lovers","casual","couples"]
        },
        {
            "id":"RS104",
            "name": "Pierre Hermé Paris",
            "cuisine": "Pastry & Dessert",
            "price_range": "$$$",
            "rating": 4.8,
            "neighborhood":"Saint-Germain",
            "description":"Famous for innovative pastries, macarons, and desserts with exquisite flavors.",
            "best_for":["dessert lovers","special occasion","sweet tooth"]
        }
    ]
}

def get_flights(destination:str)->list:
    """ Get available flght for a destion"""
    return MOCK_FLIGHT.get(destination.lower(),[])

def get_hotels(destination:str)->list:
    """Get available hotels for a destination"""
    return MOCK_HOTEL.get(destination.lower(),[])

def get_activities(destination:str)->list:
    """Get available activities for a destination"""
    return MOCK_ACTIVITIES.get(destination.lower(),[])

def get_restaurants(destination:str)->list:
    """Get available restaurant for a destination"""
    return MOCK_RESTAURANTS.get(destination.lower(),[])

