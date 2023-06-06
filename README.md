# CodingChallengeKIN

## Explanation of the settings.json
To enable the user to change the values of the simulation without programming knowledge, the `settings.json` provides the possibility to edit the settings outside the code.  

`zmq:address` - ip address of the host  
`zmq:port` - port for communication  

`game:player_count` - amount of players/sensors  
`game:updates_per_second` - sending frequency in Hz  

`field:width` - width of the field in meters  
`field:height` - height of the field in meters  

`player:max_speed` - maximum speed of players in meters/second  

`visualisation:width` - amount of pixels in x direction  
`visualisation:height` - amount of pixels in y direction  
`visualisation:point_size` - size of the shown players on screen in pixels  
`visualisation:color` - color of the shown pixels in BGR-format  

`quality_control:color` - color of the shown players in BGR-format  
