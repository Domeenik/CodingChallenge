# CodingChallengeKIN

## Explanation of the settings.json
To enable the user to change the values of the simulation without programming knowledge, the `settings.json` provides the possibility to edit the settings outside the code.  

### Parameters
`zmq:address` - ip address of the host  
`zmq:port` - port for communication  
`game:player_count` - amount of players/sensors  
`game:updates_per_second` - sending frequency in Hz  
`field:width` - width of the field in meters  
`field:height` - height of the field in meters  
`player:max_speed` - maximum speed of players in meters/second  
`player:boid_behavior` - enables a bit more complex movement pattern  
`player:sight` - vision range for player (boid behavior only)  
`player:alignment` - factor for the alignment to the neighbors (boid behavior only)  
`player:coherence` - factor how much the position of other players is targeted (boid behavior only)  
`player:separation` - factor how much is repelled by the other players (boid behavior only)  
`visualisation:width` - amount of pixels in x direction  
`visualisation:height` - amount of pixels in y direction  
`visualisation:point_size` - size of the shown players on screen in pixels  
`visualisation:player_color` - color of the players in BGR-format  
`visualisation:background_color` - color of the background in BGR-format  
`quality_control:max_excessive_time_percent` - Percentage maximum of the transmission frequency that may be exceeded before a warning is displayed  
