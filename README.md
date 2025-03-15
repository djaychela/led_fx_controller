# LedFX Controller

<a id="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#installation">Installation As a Service</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a development of my Wedding Controller project.  The original project was much more complex than this, involving automation of changing effects with voted-on songs and colours related to each voter.  

Running LedFX at home with the lights I made for the disco is something I like doing, but the original project has a lot more complexity than is now needed - with extra API calls, a song database which is no longer needed and so on, so this is an attempt to just provide a way of automating changes to LedFX to suit the music which is playing - the aim is to have the system detect what song is playing on my local Sonos system, and to change effect and colours when the track changes.

API Endpoints are set in `config.py` - there is one for this system, one for LedFX. 

To get this up and running all on the same system, just change the IP addresses of the endpoints to `127.0.0.1` and you should be good to go - LedFX happily co-exists with this on my M1 macbook.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [LedFX](https://github.com/LedFx/LedFx)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Requests](https://pypi.org/project/requests/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Mixxx](https://mixxx.org/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Running install of LedFX, with lights setup as a virtual, and running in audio-reactive mode.  

### Installation

This installation was to get the script running on a Raspberry Pi - the same one that is running LedFX, allowing these controls to be used via a web browser.

1. Create a Python 3.11 virtual environment 
   ```sh
   mkdir ledfx_ctrl
   cd ledfx_ctrl
   python3 -m venv fastapi-env
   source fastapi-env/bin/activate # linux/macOS
   fastapi-env/Scripts/activate.bat # windows
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/djaychela/led_fx_controller.git
   ```
3. Install python dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```
4. Change the `API_BASE_URL` and `FX_CTRL_BASE_URL` constants appropriately in `config.py` - for instance for a setup with LedFX running on the same machine as the wedding controller (the default), but if you have it on another machine then this would need to change, such as here (for the original setup where it was on another machine with the IP address seen)
   ```python
   API_BASE_URL = "http://192.168.1.238:8888"
   ```

5. Run the Controller.  You can do this with Uvicorn or similar, but for testing the FastAPI server will do:

   ```sh
   fastapi dev controller/main.py 
   ```
6. Endpoints defined are now accessible in a browser, such as

    ```
    http://192.168.1.238:8000/state/change_effect
    ```
    Which will change the effect currently running in LedFX
7. There is a simple web front end available at the base URL.  This allows selection of random colour gradient, a single colour, a single-colour gradient, random effect and random effect preset.

    ```
    http://192.168.1.238:8000/state/change_effect
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation As a Service

This app is designed to run without any further user intervention.  On a Pi set up to run LedFX on boot, the web front end also needs to do this.  Settings for this can be a little difficult to find, but it's generally a case of creating a service file with the right settings, and then enabling this service.  Then the system will run uvicorn (the web server) for the project out-of-the-box. It's not a heavy-duty reverse-proxy server or similar, but it's fine for a single user to use on an app in their home network, so that's why I've included it here (as it took me a while to pull all this together and get the right settings).  You'll need to change the path in the given `uvicorn-fastapi.service` file to suit your home directory and user name.

1. Create the system service file in an editor:

  ```
  sudo nano /etc/systemd/system/uvicorn-fastapi.service
  ```
2. Enter the following contents, altering the username, group, working directory and exec start entries to suit your pi's username and location of the files (if you've worked from the home directory the only thing you'll need to do is replace `darren` with your username in all four of these).

  ```
  [Unit]
  Description=Uvicorn
  After=network.target

  [Service]
  Type=simple
  User=darren
  Group=darren
  DynamicUser=true
  WorkingDirectory=/home/darren/ledfx_ctrl/led_fx_controller
  PrivateTmp=true
  ExecStart=/home/darren/ledfx_ctrl/fastapi-env/bin/uvicorn \
          --proxy-headers \
          --forwarded-allow-ips='*' \
          --workers=4 \
          --host=0.0.0.0 \
          --port=8000 \
          --no-access-log \
          controller.main:app
  ExecReload=/bin/kill -HUP ${MAINPID}
  RestartSec=1
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

3. Reload the daemon service to enable new files (you need to do this if you edit this file, you may not initally but it's good to know)

  ```
  sudo systemctl daemon-reload
  ```

4. Enable the newly-created service:

  ```
  sudo systemctl enable uvicorn-fastapi.service 
  ```

5. Start the service:

  ```
  sudo systemctl start uvicorn-fastapi.service 
  ```

6. Check the service status:

  ```
  sudo systemctl status uvicorn-fastapi.service
  ```

  You should see something similar to this:

  ```
  ● uvicorn-fastapi.service - Uvicorn
     Loaded: loaded (/etc/systemd/system/uvicorn-fastapi.service; enabled; preset: enabled)
     Active: active (running) since Fri 2025-03-14 20:14:34 GMT; 6s ago
   Main PID: 1717 (uvicorn)
      Tasks: 18 (limit: 9259)
        CPU: 5.842s
     CGroup: /system.slice/uvicorn-fastapi.service
  ```

  If you see errors, then you'll need to go back to step 2, ensuring paths are correct.  
  Once the service is running, it will run the web app every time the Pi starts.

<!-- USAGE EXAMPLES -->
## Usage

To set this up locally, ensure that `API_BASE_URL` in `config.py` is set to point at `127.0.0.1:8888`, and set up a virtual in LedFX, called virtual-1.  

System can be [seen running here](https://photos.app.goo.gl/MPWkFfHzNgioq3M98)

There's a fair bit of output to the console as the system runs.  This was for bug-hunting initially but I left it in place as the system needed to work out-of-the-box on my wedding day and having the reassurance of seeing this output on the morning was very relaxing!  This can be disabled by setting `CONSOLE_OUTPUT` to `False` in `config.py`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

This is a legacy project that I've posted and made public because I was asked about it in an HN thread, and because I'm terminally ill and thought it might be useful to someone someday.

As a result, contributions are not open!  Feel free to fork the project and work on it, improve it or just use it.  But there isn't an active project as such because of my health.

### Top contributors:

<a href="https://github.com/djaychela/wedding_controller/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=djaychela/wedding_controller" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The project worked because of these two great projects - LedFX as a controller and WLED which runs the lights that LedFX controls.

* [LedFX](https://github.com/ledfx/ledfx)
* [Wled](https://kno.wled.ge/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

