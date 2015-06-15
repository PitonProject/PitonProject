# PitonProject
Aplicació desenvolupada per <a href="https://github.com/sanchezfauste">Marc Sánchez</a> i <a href="https://github.com/ferranverdes">Ferran Verdés</a>

La idea principal de l'aplicació és que els usuaris d'un pub puguin escollir la música que volen que hi soni. Concretament, es tracta d'una app que permet a un usuari seguir als seus pubs de preferència, consultar les playlists de música que aquest té associades i afegir-hi cançons, tot partint del repertori de música que s'ofereix a la plataforma Spotify.

## API RESTful
<table>
  <tr>
    <th>Method</th>
    <th>Resource</th>
    <th>Description</th>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/pub</td>
    <td>Llistat de pubs registrats en format HTML</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/pub.json</td>
    <td>Llistat de pubs registrats en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/pub.xml</td>
    <td>Llistat de pubs registrats en format XML</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/pub/id</td>
    <td>Informació d'un pub en format HTML</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/pub/id.json</td>
    <td>Informació d'un pub en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/pub/id.xml</td>
    <td>Informació d'un pub en format XML</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/pub/id/playlist.json</td>
    <td>Llistat de playlists que té registrades un pub en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/pub/id/playlist.xml</td>
    <td>Llistat de playlists que té registrades un pub en format XML</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/playlist</td>
    <td>Llistat de playlists registrades en format HTML</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/playlist.json</td>
    <td>Llistat de playlists registrades en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/playlist.xml</td>
    <td>Llistat de playlists registrades en format XML</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/playlist/id</td>
    <td>Informació d'una playlist en format HTML</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/playlist/id.json</td>
    <td>Informació d'una playlist en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/playlist/id.xml</td>
    <td>Informació d'una playlist en format XML</td>
  </tr>

  <tr>
    <td>GET</td>
    <td>/playlist/id/track.json</td>
    <td>Llistat de cançons que té una playlist en format Json</td>
  </tr>  
  <tr>
    <td>GET</td>
    <td>/playlist/id/track.xml</td>
    <td>Llistat de cançons que té una playlist en format XML</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>/track</td>
    <td>Llistat de tracks registrats en format HTML</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/track.json</td>
    <td>Llistat de tracks registrats en format Json</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/track.xml</td>
    <td>Llistat de tracks registrats en format XML</td>
  </tr>
</table>

També s'ofereix una API RESTful a `/api`, en la qual només pot accedir-hi un usuari administrador. Aquesta API està implementada fent ús del Django REST framework.

## Panell d'administració
El projecte inclou una base de dades SQLite per tal de poder provar-lo.
Per accedir al panel d'administració s'ha d'accedir a `/admin`.
L'usuari administrador és: `admin` amb password: `123456`

## Funcionament general
Quan accedim a la pàgina principal, una vegada hem superat el procés de login, podem veure la llista de pubs que seguim (amb l'objectiu de participar al seu reportori musical). A l'esquerra de la pàgina hi trobarem el menú principal de navegació, el qual ens permetrà accedir a les diferents seccions que hem implementat, com per exemple, a la de "Add track to pub playlist", la qual ens permet afegir una cançó a la playlist d'un pub, tot mitjançant la cerca d'aquesta dins de la plataforma de Spotify.
