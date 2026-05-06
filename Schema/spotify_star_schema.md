#   Spotify Data Warehouse Schema


## Overview
This Star Schema is designed for the Spotify Data warehouse.
It enable analysis of track popularity, artist performance and genre trends across 114,000 tracks.


## Schema Diagram                                                                    
                                        ┌──────────────────────┐                                   
                                        │                      │                                   
                                        │     Fact_track       │                                   
      ┌────────────────┐                ┼──────────────────────┤          ┌─────────────────┐      
      │ dim_tracks     │                │                      │          │                 │      
      │                ┼────────────────┼──►track_id           │   ┌──────┼─dim_albums      │      
      └────────────────┘                │                      │   │      │                 │      
                               ┌────────┼─► artist_id          │   │      └─────────────────┘      
                               │        │                      │   │                               
                               │        │   album_id  ◄────────┼───┘                               
       ┌───────────────┐       │        │                      │                                   
       │               │       │        │   genre_id  ◄────────┼──┐      ┌───────────────────┐     
       │ dim_artists   ┼───────┘        │                      │  │      │                   │     
       │               │                │   fact_id            │  └──────┼────dim_genres     │     
       └───────────────┘                │                      │         │                   │     
                                        └──────────────────────┘         └───────────────────┘     


## Table
### fact_tracks
| Column           | Type   | Constraint  |
|------------------|--------|-------------|
| track_id         | INT    |     FK      |
| artist_id        | INT    |     FK      |                                                           
| album_id         | INT    |     FK      |
| genre_id         | INT    |     FK      |
| fact_id          | INT    |     PK      |
| popularity       | INT    |             |
| duration_ms      | INT    |             |
| danceability     | Float  |             |
| energy           | Float  |             |
| key              | INT    |             |
| loudness         | Float  |             |
| mode             | INT    |             |
| speechiness      | Float  |             |
| acousticness     | Float  |             |
| instrumentalness | Float  |             |
| liveness         | Float  |             |
| valence          | Float  |             |
| tempo            | Float  |             |
| time_signature   | INT    |             |

## dim_tracks
| Column           | Type         | Constraint  |
|------------------|--------------|-------------|
| track_id         | CHAR(22)     |     PK      |
| track_name       | VARCHAR(255) |             |
| explicit         | BOOLEAN      |             |

## dim_albums
| Column           | Type         | Constraint  |
|------------------|--------------|-------------|
| album_id         | CHAR(22)     |     PK      |
| album_name       | VARCHAR(255) |             |

## dim_artists
| Column            | Type         | Constraint  |
|-------------------|--------------|-------------|
| artist_id         | CHAR(22)     |     PK      |
| artist_name       | VARCHAR(255) |             |

## dim_genre
| Column            | Type         | Constraint  |
|-------------------|--------------|-------------|
| genre_id          | CHAR(22)     |     PK      |
| track_genre       | VARCHAR(255) |             |