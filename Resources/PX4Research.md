## Primary Library/Software: PX4

The recommended hardware is pixhawk.

QGroundControl is used for flight control and vehicle setup
    And mission planning :)
    Have to research QGroundControl & AirSim together

Minimum Hardware Requirements:
    1. Gyroscope
    2. Accelerometer
    3. Magnetometer/Compass
    4. Barometer
    5. GPS / Positioning System

Outputs should be PWM ports or DroneCAN

Can connect any output to any motor by assigning function to output in GroundControl

FMU Output Ports can use D-Shot/One-Shot protocols which are lower latency

Default only 6-8 outputs in Main/Aux, in theory there can be more

SD Cards required for storing flight logs, use UAVCAN peripherals, and autonomous flight
    Max supported size is 32gb

Can have flight modes, if we want

Has failsafes we can check for and ignore if we want to

Will need strong standalone camera control

Trigger Interface Backends: Use 1, GPIO interface, can be used to trigger most cameras
    Should work with OpenCV then?

## Future Research
- MAVLink
    - https://mavlink.io/en/
    - Combining with OpenCV
    - https://mavsdk.mavlink.io/main/en/index.html
- QGroundControl