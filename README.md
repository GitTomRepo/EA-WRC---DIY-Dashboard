# EA WRC- DIY-Dashboard

The major goal of this target is to make a DIY dashboard for the game EA WRC.
With the update v1.3, we seen the UDP telemetry add to the game. So the main idea here is to get that UDP trafic into a TFT screen display.

The main things to achieve this task are :
  1. Configure correctly the UDP data to get ONLY the important informations (for example : we do not care about the vehicule coord on the map, for the moment ...)
  2. Get that UDP trafic with a python script
  3. Process the bytes tab to get all the (essential) informations
  4. Send these datas to an Arduino UNO
  5. Transform these datas into a TFT screen display (tricky UI here ...)
  6. Enjoy the dashboard now !

I am new here with UDP protocol, and not familiar with the socket packet on python... So please be cool, and if you find better way to do things (like get this f*****g UDP bytes) do a pull 
