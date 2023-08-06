===================
Python digimat.bac0
===================

This is a Python 3 module basically providing a wrapper around the [BAC0] (https://bac0.readthedocs.io/en/latest/) module, 
itself using [bacpypes] (https://github.com/JoelBender/bacpypes), allowing to access and browse BACnet/IP networks. The main goal of this module id to provide
a simple way to discover/browse/interact with BACnet/IP devices on a network. Install this module with a *pip install -U digimat.bac0* command.

.. code-block:: python

    >>> from digimat.bac0 import BAC
    >>> bacnet=BAC(network='192.168.0.84/24')

Congratulations ! You just have launched a BACnet/IP node binded to your LAN card (ip 192.168.0.84, netmask 255.255.255.0). The underlying BAC0 module has started a thread managing
the remote bacnet nodes (understand remote "BACnet servers") you will declare to your node. You have to provide the ip ("ip/networkSize") that will be used to send/receive 
every BACnet UDP messages. Under Linux/MacOS hots, this can be done automagically if you have installed the [netifaces] (https://pypi.org/project/netifaces/) module. If so, you can
ommit the *network* parameter

.. code-block:: python

    >>> bacnet=BAC() # return a BAC object
    >>> bacnet
    <BAC:192.168.0.84/24(0 devices)>

If needed, you can give a bbmd router ('ipAddress[:port]') to the constructor

.. code-block:: python

    >>> bacnet=BAC(router='192.168.2.1')

Now, assuming that your network settings are correct, you can start discovering the network

.. code-block:: python

    >>> bacnet.whois()      # return a list of devices detected on the network
   [('192.168.0.15', 8015), ('192.168.0.80', 4000)]

The *whois()* method returns a list of remote BACnet/IP servers detected on the network (ip/deviceId). TYou can then can add to your node thoses remote *devices* (BACnet servers)

.. code-block:: python

    >>> device=bacnet.declareDevice(8015, '192.168.0.15')

In fact, if the device is detected by the whois(), you can declare a node based on it's id or it's ip address

.. code-block:: python

    >>> device=bacnet.declareDevice(8015) # return a BACDevice object
    >>> device=bacnet.declareDevice('192.168.0.15') # equivalent
    >>> device
    <BACDevice:8015#0(Digimat:Digimat3_CPU_Bridge, operational, 66 points)>

    >>> bacnet.discover()# this will magically declare ebery whois() device

Every BAC* object has a .dump() method, very useful in interactive sessions

.. code-block:: python

    >>> bacnet.dump()
    +---+---------+------+--------------+---------+---------------------+-------------+-------------+---------+
    | # | name    |  id  |      ip      | vendor  | model               |    status   | description | #points |
    +---+---------+------+--------------+---------+---------------------+-------------+-------------+---------+
    | 0 | s_112_1 | 8015 | 192.168.0.15 | Digimat | Digimat3_CPU_Bridge | operational | S+T         |    66   |
    +---+---------+------+--------------+---------+---------------------+-------------+-------------+---------+

    >>> device.dump()
    +-----------------------+--------------+
    | property              | value        |
    +-----------------------+--------------+
    | ip                    | 192.168.0.15 |
    | id                    | 8015         |
    | name                  | s_112_1      |
    | description           | S+T          |
    | systemStatus          | operational  |
    | vendorName            | Digimat      |
    | vendorIdentifier      | 892          |
    | points                | 66           |
    | segmentationSupported | True         |
    | analogInput           | 16           |
    | analogOutput          | 8            |
    | binaryInput           | 31           |
    | binaryOutput          | 11           |
    +-----------------------+--------------+

Ocne a device has been declared, you can retrieve it with bacnet.device(...) or directly with a bacnet[...] request. You can use either the index (0), the name (s_112_1), the id (8105) or the ip (192.168.0.15) 
to retrieve your device from the BAC object. If you redeclare a device already existing, it will be simply returned (not duplicated).

You will have to dig a bit into the *BAC* and *BACDevice* objects to find avalaible methods and properties. It's now time to access to the points (variables) of our device, all provided
by the device.points property, returning a *BACPoints* object

.. code-block:: python

    >>> points=device.points
    >>> points
    <BACPoints(66 points)>

    >>> points.dump()
    +----+----------------------+---------------------+-------------------------------------------------------------------------+--------------+---------+----------+------+-------+-------+------+
    | #  | class                | name                | description                                                             | type         | address |    value | unit |  COV  |  OoS  | PRI  |
    +----+----------------------+---------------------+-------------------------------------------------------------------------+--------------+---------+----------+------+-------+-------+------+
    | 0  | BACPointAnalogInput  | r_112_1_cio_13056_0 | sonde exterieure                                                        | analogInput  |   13056 |    38.51 | C    | False | False | None |
    | 1  | BACPointAnalogInput  | r_112_1_cio_13057_0 | sonde depart chaudiere                                                  | analogInput  |   13057 |    26.07 | C    | False | False | None |
    | 2  | BACPointAnalogInput  | r_112_1_cio_13058_0 | sonde depart radiateurs                                                 | analogInput  |   13058 |    31.20 | C    | False | False | None |
    | 3  | BACPointAnalogInput  | r_112_1_cio_13059_0 | sonde depart chauffage de sol                                           | analogInput  |   13059 |    27.10 | C    | False | False | None |
    | 4  | BACPointAnalogInput  | r_112_1_cio_13060_0 | pot.physique consigne depart chauffage de sol (-10;+10C)                | analogInput  |   13060 |     4.91 | C    | False | False | None |
    | 5  | BACPointAnalogInput  | r_112_1_cio_13061_0 | pot.physique consigne depart radiateurs (-10;+10C)                      | analogInput  |   13061 |     2.93 | C    | False | False | None |
    | 6  | BACPointAnalogInput  | r_112_1_cio_13062_0 | sonde ambiance bureau direction rez                                     | analogInput  |   13062 |    26.26 | C    | False | False | None |
    | 7  | BACPointAnalogInput  | r_112_1_cio_13063_0 | pot.temperature bureau direction rez                                    | analogInput  |   13063 |    21.56 | C    | False | False | None |
    | 8  | BACPointAnalogInput  | r_112_1_cio_13064_0 | sonde ambiance bureau direction cote hall rez                           | analogInput  |   13064 |    26.40 | C    | False | False | None |
    | 9  | BACPointAnalogInput  | r_112_1_cio_13065_0 | pot.temperature bureau direction cote hall rez                          | analogInput  |   13065 |    21.71 | C    | False | False | None |
    | 10 | BACPointAnalogInput  | r_112_1_cio_13066_0 | sonde ambiance salle de conferences                                     | analogInput  |   13066 |    27.81 | C    | False | False | None |
    | 11 | BACPointAnalogInput  | r_112_1_cio_13067_0 | sonde ambiance temperature bureau comptabilite  rez                     | analogInput  |   13067 |    25.85 | C    | False | False | None |
    | 12 | BACPointAnalogInput  | r_112_1_cio_13068_0 | sonde ambiance bureau schematique s-sol                                 | analogInput  |   13068 |    24.23 | C    | False | False | None |
    | 13 | BACPointAnalogInput  | r_112_1_cio_13069_0 | pot.temperature bureau schematique s-sol                                | analogInput  |   13069 |    21.00 | C    | False | False | None |
    | 14 | BACPointAnalogInput  | r_112_1_cio_13070_0 | sonde ambiance bureau individuel s-sol                                  | analogInput  |   13070 |    25.86 | C    | False | False | None |
    | 15 | BACPointAnalogInput  | r_112_1_cio_13071_0 | pot.temperature bureau individuel s-sol                                 | analogInput  |   13071 |    20.40 | C    | False | False | None |
    | 16 | BACPointAnalogOutput | r_112_1_cio_18176_0 | vanne depart radiateurs                                                 | analogOutput |   18176 |     0.00 | %    | False | False |  16  |
    | 17 | BACPointAnalogOutput | r_112_1_cio_18177_0 | vanne depart general chauffage de sol                                   | analogOutput |   18177 |     0.00 | %    | False | False |  16  |
    | 18 | BACPointAnalogOutput | r_112_1_cio_18178_0 | vannes depart chauffage de sol bureau direction rez                     | analogOutput |   18178 |     0.00 | %    | False | False |  16  |
    | 19 | BACPointAnalogOutput | r_112_1_cio_18179_0 | vanne depart chauffage de sol bureau direction cote hall rez            | analogOutput |   18179 |     0.00 | %    | False | False |  16  |
    | 20 | BACPointAnalogOutput | r_112_1_cio_18180_0 | vanne depart chauffage de sol bureau comptabilite rez                   | analogOutput |   18180 |     0.00 | %    | False | False |  16  |
    | 21 | BACPointAnalogOutput | r_112_1_cio_18181_0 | vanne depart chauffage de sol bureau schematique s-sol                  | analogOutput |   18181 |     0.00 | %    | False | False |  16  |
    | 22 | BACPointAnalogOutput | r_112_1_cio_18182_0 | vanne depart chauffage de sol bureau individuel s-sol                   | analogOutput |   18182 |     0.00 | %    | False | False |  16  |
    | 23 | BACPointAnalogOutput | r_112_1_cio_18183_0 | consigne puissance bruleur                                              | analogOutput |   18183 |     5.00 | %    | False | False |  16  |
    | 24 | BACPointBinaryInput  | r_112_1_cio_256_0   | circulateur depart radiateurs                                           | binaryInput  |     256 | inactive | None | False | False | None |
    | 25 | BACPointBinaryInput  | r_112_1_cio_257_0   | thermique circulateur depart radiateurs                                 | binaryInput  |     257 | inactive | None | False | False | None |
    | 26 | BACPointBinaryInput  | r_112_1_cio_258_0   | circulateur depart chauffage de sol                                     | binaryInput  |     258 | inactive | None | False | False | None |
    | 27 | BACPointBinaryInput  | r_112_1_cio_259_0   | thermique circulateur depart chauffage de sol                           | binaryInput  |     259 | inactive | None | False | False | None |
    | 28 | BACPointBinaryInput  | r_112_1_cio_260_0   | coffret pompe fosse eaux usees chaufferie                               | binaryInput  |     260 | inactive | None | False | False | None |
    | 29 | BACPointBinaryInput  | r_112_1_cio_261_0   | effraction bureau direction rez (capteur a fil)                         | binaryInput  |     261 | inactive | None | False | False | None |
    | 30 | BACPointBinaryInput  | r_112_1_cio_262_0   | effraction bureau comptabilite rez (capteur a fil)                      | binaryInput  |     262 | inactive | None | False | False | None |
    | 31 | BACPointBinaryInput  | r_112_1_cio_263_0   | effraction bureau schematique chaufferie + saleve s-sol (capteur a fil) | binaryInput  |     263 | inactive | None | False | False | None |
    | 32 | BACPointBinaryInput  | r_112_1_cio_264_0   | effraction stock s-sol (capteur a fil)                                  | binaryInput  |     264 | inactive | None | False | False | None |
    | 33 | BACPointBinaryInput  | r_112_1_cio_265_0   | effraction bureau construction rez (capteur a fil)                      | binaryInput  |     265 | inactive | None | False | False | None |
    | 34 | BACPointBinaryInput  | r_112_1_cio_266_0   | alarme feu sur canal 1 recepteur (transmetteurs a ondes)                | binaryInput  |     266 | inactive | None | False | False | None |
    | 35 | BACPointBinaryInput  | r_112_1_cio_267_0   | effraction divers detecteurs IR interieur (capteurs sans fil)           | binaryInput  |     267 | inactive | None | False | False | None |
    | 36 | BACPointBinaryInput  | r_112_1_cio_268_0   | mouvement divers detecteurs IR exterieur (capteurs sans fil)            | binaryInput  |     268 | inactive | None | False | False | None |
    | 37 | BACPointBinaryInput  | r_112_1_cio_269_0   | effraction porte d'entree rez (capteur a fil)                           | binaryInput  |     269 | inactive | None | False | False | None |
    | 38 | BACPointBinaryInput  | r_112_1_cio_270_0   | interrupteur a cle 1 (activation du systeme de surveillance)            | binaryInput  |     270 | inactive | None | False | False | None |
    | 39 | BACPointBinaryInput  | r_112_1_cio_271_0   | sabotage interrupteur a cle                                             | binaryInput  |     271 | inactive | None | False | False | None |
    | 40 | BACPointBinaryInput  | r_112_1_cio_272_0   | fusibles de commande                                                    | binaryInput  |     272 | inactive | None | False | False | None |
    | 41 | BACPointBinaryInput  | r_112_1_cio_273_0   | delestage SI tbl. Tableau chaufferie                                    | binaryInput  |     273 | inactive | None | False | False | None |
    | 42 | BACPointBinaryInput  | r_112_1_cio_274_0   | temperature depart chauffage de sol                                     | binaryInput  |     274 | inactive | None | False | False | None |
    | 43 | BACPointBinaryInput  | r_112_1_cio_275_0   | temperature gas cheminee                                                | binaryInput  |     275 | inactive | None | False | False | None |
    | 44 | BACPointBinaryInput  | r_112_1_cio_276_0   | alarme feu chaufferie (capteur a fil)                                   | binaryInput  |     276 | inactive | None | False | False | None |
    | 45 | BACPointBinaryInput  | r_112_1_cio_277_0   | interrupteur a cle 2 - poussoir (quittance sirene) (hors-service)       | binaryInput  |     277 | inactive | None | False | False | None |
    | 46 | BACPointBinaryInput  | r_112_1_cio_278_0   | niveau haut fosse eau pluviale cote jardin                              | binaryInput  |     278 | inactive | None | False | False | None |
    | 47 | BACPointBinaryInput  | r_112_1_cio_279_0   | effraction salle de conferences rez (capteur a fil)                     | binaryInput  |     279 | inactive | None | False | False | None |
    | 48 | BACPointBinaryInput  | r_112_1_cio_512_0   | Thermique pompe de fosse eau pluviale cote parking                      | binaryInput  |     512 | inactive | None | False | False | None |
    | 49 | BACPointBinaryInput  | r_112_1_cio_513_0   | Pompe de fosse eau pluviale cote parking                                | binaryInput  |     513 | inactive | None | False | False | None |
    | 50 | BACPointBinaryInput  | r_112_1_cio_514_0   | Interrupteur pompe de fosse eau pluviale cote parking                   | binaryInput  |     514 |   active | None | False | False | None |
    | 51 | BACPointBinaryInput  | r_112_1_cio_515_0   | niveau haut fosse eau pluviale cote parking                             | binaryInput  |     515 | inactive | None | False | False | None |
    | 52 | BACPointBinaryInput  | r_112_1_cio_516_0   | Surveillance tension coffret fosse eau pluviale cote parking            | binaryInput  |     516 | inactive | None | False | False | None |
    | 53 | BACPointBinaryInput  | r_112_1_cio_534_0   | entree test 1                                                           | binaryInput  |     534 |   active | None | False | False | None |
    | 54 | BACPointBinaryInput  | r_112_1_cio_535_0   | entree TEST 2                                                           | binaryInput  |     535 |   active | None | False | False | None |
    | 55 | BACPointBinaryOutput | r_112_1_cio_7937_0  | cmd.bouilleur                                                           | binaryOutput |    7937 | inactive | None | False | False |  16  |
    | 56 | BACPointBinaryOutput | r_112_1_cio_7938_0  | cmd.circulateur depart radiateurs                                       | binaryOutput |    7938 | inactive | None | False | False |  16  |
    | 57 | BACPointBinaryOutput | r_112_1_cio_7939_0  | cmd.circulateur depart chauffage de sol                                 | binaryOutput |    7939 | inactive | None | False | False |  16  |
    | 58 | BACPointBinaryOutput | r_112_1_cio_7941_0  | cmd.ventilateur extraction local chaufferie s-sol                       | binaryOutput |    7941 |   active | None | False | False |  16  |
    | 59 | BACPointBinaryOutput | r_112_1_cio_8192_0  | cmd.feu tournant                                                        | binaryOutput |    8192 | inactive | None | False | False |  16  |
    | 60 | BACPointBinaryOutput | r_112_1_cio_8193_0  | cmd.sirene                                                              | binaryOutput |    8193 | inactive | None | False | False |  16  |
    | 61 | BACPointBinaryOutput | r_112_1_cio_8194_0  | cmd.tonalite sirene                                                     | binaryOutput |    8194 | inactive | None | False | False |  16  |
    | 62 | BACPointBinaryOutput | r_112_1_cio_8195_0  | cmd.led activation (rouge)                                              | binaryOutput |    8195 | inactive | None | False | False |  16  |
    | 63 | BACPointBinaryOutput | r_112_1_cio_8196_0  | cmd.PAC salle de conferences                                            | binaryOutput |    8196 | inactive | None | False | False |  16  |
    | 64 | BACPointBinaryOutput | r_112_1_cio_8197_0  | cmd.radiateur electrique salle de conferences                           | binaryOutput |    8197 | inactive | None | False | False |  16  |
    | 65 | BACPointBinaryOutput | r_112_1_cio_8198_0  | TEST LCH                                                                | binaryOutput |    8198 |   active | None | False | False |  16  |
    +----+----------------------+---------------------+-------------------------------------------------------------------------+--------------+---------+----------+------+-------+-------+------+

    >>> device.points.dump('sonde') # output can be filtered (by part of names or descriptions)
    +----+---------------------+---------------------+-----------------------------------------------------+-------------+---------+-------+------+-------+-------+------+
    | #  | class               | name                | description                                         | type        | address | value | unit |  COV  |  OoS  | PRI  |
    +----+---------------------+---------------------+-----------------------------------------------------+-------------+---------+-------+------+-------+-------+------+
    | 0  | BACPointAnalogInput | r_112_1_cio_13056_0 | sonde exterieure                                    | analogInput |   13056 | 38.42 | C    | False | False | None |
    | 1  | BACPointAnalogInput | r_112_1_cio_13057_0 | sonde depart chaudiere                              | analogInput |   13057 | 26.07 | C    | False | False | None |
    | 2  | BACPointAnalogInput | r_112_1_cio_13058_0 | sonde depart radiateurs                             | analogInput |   13058 | 31.20 | C    | False | False | None |
    | 3  | BACPointAnalogInput | r_112_1_cio_13059_0 | sonde depart chauffage de sol                       | analogInput |   13059 | 27.12 | C    | False | False | None |
    | 6  | BACPointAnalogInput | r_112_1_cio_13062_0 | sonde ambiance bureau direction rez                 | analogInput |   13062 | 26.24 | C    | False | False | None |
    | 8  | BACPointAnalogInput | r_112_1_cio_13064_0 | sonde ambiance bureau direction cote hall rez       | analogInput |   13064 | 26.43 | C    | False | False | None |
    | 10 | BACPointAnalogInput | r_112_1_cio_13066_0 | sonde ambiance salle de conferences                 | analogInput |   13066 | 27.81 | C    | False | False | None |
    | 11 | BACPointAnalogInput | r_112_1_cio_13067_0 | sonde ambiance temperature bureau comptabilite  rez | analogInput |   13067 | 25.81 | C    | False | False | None |
    | 12 | BACPointAnalogInput | r_112_1_cio_13068_0 | sonde ambiance bureau schematique s-sol             | analogInput |   13068 | 24.23 | C    | False | False | None |
    | 14 | BACPointAnalogInput | r_112_1_cio_13070_0 | sonde ambiance bureau individuel s-sol              | analogInput |   13070 | 25.88 | C    | False | False | None |
    +----+---------------------+---------------------+-----------------------------------------------------+-------------+---------+-------+------+-------+-------+------+

Each point of the *BACPoints* object is accessible by it's index, type or a part of *something belonging* to it 

.. code-block:: python

    >>> point=points[8]
    >>> point
    <BACPointAnalogInput(r_112_1_cio_13064_0:analogInput#13064=26.51 degreesCelsius)>

    >>> point.dump()
    +--------------+-----------------------------------------------+
    | property     | value                                         |
    +--------------+-----------------------------------------------+
    | class        | BACPointAnalogInput                           |
    | name         | r_112_1_cio_13064_0                           |
    | description  | sonde ambiance bureau direction cote hall rez |
    | type         | analogInput                                   |
    | address      | 13064                                         |
    | value        | 26.57267189025879                             |
    | state        | 26.57                                         |
    | unit         | degreesCelsius (C)                            |
    | COV          | False                                         |
    | OutOfService | False                                         |
    | index        | 8                                             |
    +--------------+-----------------------------------------------+

    >>> point=device.points.analogInput(13056)
    >>> point=bacnet[8015].points.analogOuput(18181)

    >>> points['sonde hall'] # return the first object matching to this
    <BACPointAnalogInput(r_112_1_cio_13064_0:analogInput#13064=26.55 degreesCelsius)>

    >>> point=point['r_112_1_cio_13067_0']
    >>> point=point['13067']

Points are exposed through *BACPoint* objects (generic class), derived in BACPointBinaryInput, BACPointBinaryOutput, BACPointAnalogInput, BACPointAnalogOutput, BACPointBinaryValue, BACPointAnalogValue, 
BACPointMultiStateInput, BACPointMultiStateOutput, BACPointMultiStateValue objects, each providing specialized BACPoint extensions. You will have to dig a bit into theses objects to learn what helper they provide. Using
[bpython] (https://bpython-interpreter.org/) interactive interpreter with it's autocompletion feature is a very convenient way to discover thoses object (with the actual lack of documentation)

.. code-block:: python

    >>> point.
    ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ activePriority               address                      bacnetProperty               bacnetproperties             celciusToFahrenheit          cov                                          │
    │ covCancel                    description                  digDecimals                  digUnit                      digUnitStr                   dump                                         │
    │ fahrenheitToCelcius          index                        isAnalog                     isBinary                     isCOV                        isMultiState                                 │
    │ isOutOfService               isWritable                   label                        match                        name                         onInit                                       │
    │ poll                         pollStop                     priority                     properties                   read                         refresh                                      │
    │ reloadBacnetProperties       state                        toCelcius                    type                         unit                         unitNumber                                   │
    │ value                                                                                                                                                                                         │
    └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    >>> point.value
    26.699626922607422
    >>> point.unit
    'degreesCelsius'

    >>> point.value=12.0 # if a point is writable, this will change it's value

If a *BACPoint* doesn't expose something that would be useful, either ask it (we will try to add this support) or use the underlying point._bac0point object which is the BAC0's Point object (https://bac0.readthedocs.io/en/latest/BAC0.core.devices.html#BAC0.core.devices.Points.Point) associated to this point.

We will try to add objetcs and methods docstring as soon as possible to help the use of theses objects. Please let us know (fhess@st-sa.ch) is this is useful for someone.
