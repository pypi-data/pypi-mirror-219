=======
lolcatt
=======

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/Documentation-Github-blue
   :target: https://LokiLuciferase.github.io/lolcatt/
   :alt: Documentation

.. image:: https://github.com/LokiLuciferase/lolcatt/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/LokiLuciferase/lolcatt/actions/workflows/ci.yml
   :alt: Build Status

.. image:: https://github.com/LokiLuciferase/lolcatt/raw/python-coverage-comment-action-data/badge.svg
   :target: https://github.com/LokiLuciferase/lolcatt/raw/python-coverage-comment-action-data/badge.svg
   :alt: Coverage Status


A TUI wrapper around catt_, enabling you to cast to and control your chromecast devices.


.. image:: https://raw.githubusercontent.com/LokiLuciferase/lolcatt/master/docs/_static/screenshot.png
   :align: center
   :alt:


Dependencies
------------
- Python 3.8+
- catt_ (will be installed automatically)
- yt-dlp_ (will be installed automatically)
- Optional: A font containing FontAwesome icons to allow displaying of fancy icons on buttons. The freely available NerdFont_ collection is recommended. Fancy icons can be disabled and replaced by text (see below).


Installation
------------

.. code-block:: bash

    pip install lolcatt


Quckstart
----------

At first we need to determine the name of the chromecast device we want to cast to. To do so, run ``lolcatt --scan``.
To start the UI, run ``lolcatt -d '<device name or alias>'`` (or simply ``lolcatt`` if a default device is set).
A default device and device aliases can be set in the ``catt`` configuration file (per default under ``~/.config/catt/config.cfg``), see catt_'s documentation for more information.

To cast, paste either a URL or a path to a local file into the input field and press enter. To prepend a URL or path to the playback queue instead of playing immediately, hit Ctrl+s instead of enter. To seek, tap the progress bar.

For URLs, all websites supported by yt-dlp_ (which handles media download under the hood) are supported. Find a list of supported websites here_. For local media, most common video and image formats are supported.

Youtube playlists are supported, and each contained video will be added to the playback queue. By specifying a cookie file in the config (per default under ``~/.config/lolcatt/config.toml``), you can also access private YouTube playlists such as "Watch Later" (https://www.youtube.com/playlist?list=WL), and ensure played YouTube videos are marked as watched.


Troubleshooting
---------------

If button icons are not displayed correctly, ensure you are using a font containing FontAwesome icons. Alternatively, you can disable the use of fancy icons in the config file.

If casting does not work for no apparent reason, ensure you have the latest version of ``yt_dlp`` installed: ``pip install --upgrade yt-dlp``.

If you encounter any other issues, please open an issue.


Credits
-------

This package was created with Cookiecutter_ and the `LokiLuciferase/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/LokiLuciferase/cookiecutter
.. _`LokiLuciferase/cookiecutter-pypackage`: https://github.com/LokiLuciferase/cookiecutter-pypackage
.. _catt: https://github.com/skorokithakis/catt
.. _yt-dlp: https://github.com/yt-dlp/yt-dlp
.. _here: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
.. _NerdFont: https://www.nerdfonts.com/
