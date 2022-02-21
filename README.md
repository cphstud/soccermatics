# Soccermatics
Disse data er hentet fra [dette repo](https://github.com/statsbomb/open-data.git)<br>
Under ressources ligger en json-fil hvor alle skud er hentet ud fra La Liga (520 kampe og 12841 skud).<br>
### sample of data
Nedenstående data beskrives i [denne]("events.pdf") fil. <br>
Ideen er at man beregner vinkel og afstand til målet.<br>
Det kan bruges til en simple xG-model [forklares her](https://www.bundesliga.com/en/bundesliga/news/expected-goals-xg-model-what-is-it-and-why-is-it-useful-sportec-solutions-3177). <br>
Modellen kan så udvides med teknik, spillerens position (rolle i opstillingen) etc.<br>


|    | id                                   | location      | timestamp    |   player |   position |   team |   under_pressure |   play_pattern | end_location       | key_pass_id                          |   first_time |   technique |   body_part |   type |   outcome |   aerial_won |   one_on_one |
|---:|:-------------------------------------|:--------------|:-------------|---------:|-----------:|-------:|-----------------:|---------------:|:-------------------|:-------------------------------------|-------------:|------------:|------------:|-------:|----------:|-------------:|-------------:|
|  0 | 65f16e50-7c5d-4293-b2fc-d20887a772f9 | [111.7, 51.7] | 00:02:29.094 |     5503 |         24 |    217 |              nan |              1 | [120, 32.7, 0.2]   | b96db2cb-9123-4596-9bfc-537a645c5991 |            1 |          91 |          40 |     87 |        98 |          nan |          nan |
|  1 | b0f73423-3990-45ae-9dda-3512c2d1aff3 | [114, 27]     | 00:05:39.239 |     5211 |          6 |    217 |              nan |              1 | [120, 35, 0.9]     | b8404e6a-e89e-40fd-8a15-e91c7b460157 |            1 |          95 |          38 |     87 |        98 |          nan |          nan |
|  2 | 13b1ddab-d22e-43d9-bfe4-12632fea1a27 | [92, 34.5]    | 00:15:28.625 |     5503 |         24 |    217 |              nan |              8 | [117.8, 38.5, 0.4] | nan                                  |          nan |          93 |          38 |     87 |       100 |          nan |          nan |
|  3 | 391bfb74-07a6-4afe-9568-02a9b23f5bd4 | [109.1, 38.7] | 00:16:19.616 |     6613 |         23 |    206 |                1 |              1 | [120, 32, 1.1]     | ce7a1f84-c7fc-4c08-a859-00fb1c6ba859 |          nan |          93 |          37 |     87 |        98 |          nan |          nan |

<br>
<br>
Ved et skud er der desuden angivet en freeze_frame. Den er udeladt fra ovenstående<br>
men i dén søjle angives de omkringstående spilleres position. Man vil altså ud fra det kunne tilføje features.<br>
F.eks hvor frit målet er og om en anden medspiller evt stod bedre placeret.

```javascript[{'location': [100.3, 37.2],
  'player': {'id': 5477, 'name': 'Ousmane Dembélé'},
  'position': {'id': 16, 'name': 'Left Midfield'},
  'teammate': True},
 {'location': [99.3, 25.8],
  'player': {'id': 5246, 'name': 'Luis Alberto Suárez Díaz'},
  'position': {'id': 22, 'name': 'Right Center Forward'},
  'teammate': True},
 {'location': [94.4, 36.1],
  'player': {'id': 6632, 'name': 'Manuel Alejandro García Sánchez'},
  'position': {'id': 15, 'name': 'Left Center Midfield'},
  'teammate': False},
 {'location': [95.2, 41.8],
  'player': {'id': 6839, 'name': 'Daniel Alejandro Torres Rojas'},
  'position': {'id': 10, 'name': 'Center Defensive Midfield'},
  'teammate': False},
 {'location': [100, 43.8],
  'player': {'id': 6855, 'name': 'Guillermo Alfonso Maripán Loaysa'},
  'position': {'id': 5, 'name': 'Left Center Back'},
  'teammate': False},
 {'location': [82.5, 54.6],
  'player': {'id': 6617, 'name': 'Ibai Gómez Pérez'},
  'position': {'id': 12, 'name': 'Right Midfield'},
  'teammate': False},
 {'location': [82.4, 24.4],
  'player': {'id': 5470, 'name': 'Ivan Rakitić'},
  'position': {'id': 15, 'name': 'Left Center Midfield'},
  'teammate': True},
 {'location': [78.6, 60.5],
  'player': {'id': 6374, 'name': 'Nélson Cabral Semedo'},
  'position': {'id': 2, 'name': 'Right Back'},
  'teammate': True},
 {'location': [96.9, 36],
  'player': {'id': 6615, 'name': 'Víctor Laguardia Cisneros'},
  'position': {'id': 3, 'name': 'Right Center Back'},
  'teammate': False},
 {'location': [91.7, 45.6],
  'player': {'id': 6612, 'name': 'Rubén Duarte Sánchez'},
  'position': {'id': 6, 'name': 'Left Back'},
  'teammate': False},
 {'location': [84.8, 20.9],
  'player': {'id': 5211, 'name': 'Jordi Alba Ramos'},
  'position': {'id': 6, 'name': 'Left Back'},
  'teammate': True},
 {'location': [87.4, 35.5],
  'player': {'id': 5203, 'name': 'Sergio Busquets i Burgos'},
  'position': {'id': 13, 'name': 'Right Center Midfield'},
  'teammate': True},
 {'location': [87.3, 37.7],
  'player': {'id': 6626, 'name': 'Mubarak Wakaso'},
  'position': {'id': 13, 'name': 'Right Center Midfield'},
  'teammate': False},
 {'location': [84.6, 43.2],
  'player': {'id': 6379, 'name': 'Sergi Roberto Carnicer'},
  'position': {'id': 12, 'name': 'Right Midfield'},
  'teammate': True},
 {'location': [99.9, 30.5],
  'player': {'id': 6618, 'name': 'Martín Aguirregabiria Padilla'},
  'position': {'id': 2, 'name': 'Right Back'},
  'teammate': False},
 {'location': [117.9, 39.8],
  'player': {'id': 6629, 'name': 'Fernando Pacheco Flores'},
  'position': {'id': 1, 'name': 'Goalkeeper'},
  'teammate': False}]```
