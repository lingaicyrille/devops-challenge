# DevOps Challenge

## Background

In this challenge you are provided with the following items.

  1. Imagery Dataset

      **data/conus_20171021_20171022_30FPS.mp4** is a link to sample imagery data file from the NOAA website.
  
  2. Data Playback Service 
  
      **data_playback** is a simple service which opens the imagery video, splits each frame into an image, then publishes that image dataset with some packed metadata (width & height).  The publisher is using ZeroMQ.

      This service can be run via **python -m data_playback**.
      
  3. Data Redactor Service

      **data_redactor** is a simple service that subscribes to the playback data. It then redacts the outer frame of the image.  Then, it publishes the data on a new ZeroMQ socket.

      This service can be run via **python -m data_redactor**.

  4. Data Visualizer Service
  
      **data_visualizer** is a simple service that subscribes to the redacted data. It then presents this stream of data via a web service. 
      
      This service can be run via **python -m data_visualizer**.

When the chain of services is deployed properly you should be able to access a local website at **http://localhost:8050** and see the steam of redacted imagery.

## Goals

You are to complete the following.

  1. Create Dockerfiles to create container images with each of the services.

  2. In a README, describe what process you would put in place to verify you containers don't have vulnerabilities.

  3. Create some way to deploy the services.(ex. a script, docker compose, manifest, helm, etc.) You are encouraged to _not_ leverage '--network host', if possible.

  4. Provide brief instructions in a README on how an operator would leverage the files generated in step 3.


## Additional Information

### Environmentals

The services have the following optional environmentals.

| service         | name          | default   | description |
| --------------- | ------------- | --------- | ----------- |
| data_playback   | DATA_FILE     | ./data/NOAA_GOES_17_satellite_imagery.mp4 | Path to data file. |
| data_playback   | PLAYBACK_PORT | 5555      | Server <- Port            |
| data_playback   | PLAYBACK_HOST | *         | Server <- Accept connections from all networks |
| data_redactor   | PLAYBACK_PORT | 5555      | Client -> Port for playback service. |
| data_redactor   | PLAYBACK_PORT | localhost | Client -> Host for playback service.      |
| data_redactor   | REDACTOR_PORT | 5556      | Server <- Port
| data_redactor   | REDACTOR_PORT | *         | Server <- Accepts connections from all networks |
| data_visualizer | REDACTOR_PORT | 5556      | Client -> Port for redactor service. |
| data_visualizer | REDACTOR_PORT | localhost | Client -> Accepts connections from all networks. |

### Published Ports

The **data_visualizer** service publishes a default port of **8050** for a client to connect.
