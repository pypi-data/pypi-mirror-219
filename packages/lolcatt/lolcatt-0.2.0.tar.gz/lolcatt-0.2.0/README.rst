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

- A font containing FontAwesome icons. The freely available NerdFont_ collection is recommended.


Installation
------------

.. code-block:: bash

    pip install lolcatt


Quckstart
----------

To determine the names of local chromecast devices, run ``lolcatt --scan``.
Afterwards, run ``lolcatt --device '<device name>'`` to start the UI targeting the specified device.
A default device and device aliases can be set in the ``catt`` configuration file, see catt_'s documentation for more information.

To cast, paste either a URL or a path to a local file into the input field and press enter. To seek, tap the progress bar.

For URLs, all websites supported by yt-dlp_ (which handles media download under the hood) are supported. Find a list of supported websites here_. For local media, most common video and image formats are supported.

Youtube playlists are supported, and each contained video will be played in sequence. By specifying a cookie file in the config file (per default under ``~/.config/lolcatt/config.toml``), you can also access private YouTube playlists such as "Watch Later" (https://www.youtube.com/playlist?list=WL).


Troubleshooting
---------------

If button icons are not displayed correctly, ensure you are using a font containing FontAwesome icons. Alternatively, you can disable the use of fancy icons in the config file.

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
