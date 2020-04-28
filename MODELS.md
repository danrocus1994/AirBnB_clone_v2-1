### User

* email: string 
* password: string 
* first_name: string 
* last_name: string 
* places: relationship
* reviews: relationship

## State

* name: string
* cities: Cities related with State

## City

* state_id: string
* name: string
* places: relationship

## Amenity

* name: string

## Place

* city_id: string
* user_id: string
* name: string
* description: string
* number_rooms: integer
* number_bathrooms: integer
* max_guest: integer
* price_by_night: integer
* latitude: float
* longitude: float
* amenities: replationship


## Review

* place_id: string
* user_id: string
* text: string