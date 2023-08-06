from ..es import Provider as PersonProvider


class Provider(PersonProvider):
    formats = (
        "{{first_name}} {{last_name}} {{last_name}}",
        "{{first_name}} {{first_name}} {{last_name}}",
        "{{first_name}} {{first_name}} {{last_name}} {{last_name}}",
        "{{first_name}} {{last_name}}",
        "{{prefix}} {{first_name}} {{last_name}}",
    )

    first_names = (
        "Abel",
        "Abelardo",
        "Abigail",
        "Abraham",
        "Abril",
        "Adalberto",
        "Adán",
        "Adela",
        "Adriana",
        "Aida",
        "Alejandra",
        "Agustín",
        "Alberto",
        "Aldonza",
        "Alicia",
        "Alta  Gracia",
        "Alonso",
        "Aldo",
        "Alejandro",
        "Alfonso",
        "Alfredo",
        "Alma",
        "Alvaro",
        "Amalia",
        "Amanda",
        "Amador",
        "Amelia",
        "Ana",
        "Anabel",
        "Ana Luisa",
        "Ana María",
        "Anel",
        "Andrea",
        "Andrés",
        "Ángel",
        "Ángela",
        "Angélica",
        "Antonia",
        "Antonio",
        "Araceli",
        "Arcelia",
        "Ariadna",
        "Armando",
        "Arturo",
        "Asunción",
        "Augusto",
        "Aurora",
        "Aurelio",
        "Barbara",
        "Beatriz",
        "Berta",
        "Benito",
        "Benjamín",
        "Bernardo",
        "Bernabé",
        "Bianca",
        "Blanca",
        "Bruno",
        "Camila",
        "Camilo",
        "Caridad",
        "Carla",
        "Carlos",
        "Carlota",
        "Carmen",
        "Carolina",
        "Catalina",
        "César",
        "Cecilia",
        "Celia",
        "Citlali",
        "Clara",
        "Claudia",
        "Claudio",
        "Clemente",
        "Concepción",
        "Conchita",
        "Cornelio",
        "Cristian",
        "Cristal",
        "Cristina",
        "Cristobal",
        "Cynthia",
        "Dalia",
        "Daniel",
        "Daniela",
        "Darío",
        "David",
        "Débora",
        "Delia",
        "Diana",
        "Diego",
        "Dolores",
        "Dulce",
        "Dulce María",
        "Eduardo",
        "Elena",
        "Elias",
        "Elisa",
        "Eloisa",
        "Elsa",
        "Elvia",
        "Elvira",
        "Eloy",
        "Emilia",
        "Emiliano",
        "Emilio",
        "Enrique",
        "Eric",
        "Ernesto",
        "Esmeralda",
        "Esteban",
        "Estefanía",
        "Estela",
        "Esparta",
        "Espartaco",
        "Esperanza",
        "Estela",
        "Esther",
        "Eugenia",
        "Eugenio",
        "Eva",
        "Evelio",
        "Fabiola",
        "Federico",
        "Felipe",
        "Fernando",
        "Felix",
        "Fidel",
        "Flavio",
        "Florencia",
        "Francisco",
        "Francisco Javier",
        "Francisca",
        "Frida",
        "Gabino",
        "Gabriela",
        "Gabriel",
        "Genaro",
        "Georgina",
        "Gerardo",
        "Gerónimo",
        "Germán",
        "Gilberto",
        "Guillermina",
        "Gloria",
        "Gonzalo",
        "Graciela",
        "Gregorio",
        "Guillermo",
        "Guadalupe",
        "Gustavo",
        "Héctor",
        "Helena",
        "Hermelinda",
        "Hernán",
        "Hilda",
        "Homero",
        "Horacio",
        "Hugo",
        "Humberto",
        "Ignacio",
        "Ilse",
        "Indira",
        "Inés",
        "Irene",
        "Irma",
        "Itzel",
        "Isaac",
        "Isabel",
        "Isabela",
        "Israel",
        "Iván",
        "Ivonne",
        "Jacinto",
        "Jacobo",
        "Jaime",
        "Javier",
        "Jaqueline",
        "Jerónimo",
        "Jesús",
        "Joaquín",
        "Jonás",
        "Jorge",
        "Jorge Luis",
        "Jos",
        "José",
        "Josefina",
        "José Carlos",
        "José Eduardo",
        "José Emilio",
        "José Luis",
        "José Manuél",
        "José María",
        "Juan",
        "Juana",
        "Juan Carlos",
        "Judith",
        "Julia",
        "Julio",
        "Julio César",
        "Laura",
        "Leonardo",
        "Leonel",
        "Leonor",
        "Karla",
        "Karina",
        "Leticia",
        "Lorenzo",
        "Lucas",
        "Lilia",
        "Liliana",
        "Linda",
        "Lorena",
        "Lourdes",
        "Lucía",
        "Luisa",
        "Luz",
        "Luis",
        "Luis Miguel",
        "Luis Manuel",
        "Magdalena",
        "Manuel",
        "Marco Antonio",
        "Marcela",
        "Marcos",
        "Margarita",
        "María",
        "Marisela",
        "Marisol",
        "María del Carmen",
        "María Cristina",
        "María Elena",
        "María Eugenia",
        "María José",
        "María Luisa",
        "María Teresa",
        "Marisol",
        "Martha",
        "Mayte",
        "Mariano",
        "Mariana",
        "Mario",
        "Martín",
        "Mateo",
        "Mauro",
        "Mauricio",
        "Maximiliano",
        "Mercedes",
        "Micaela",
        "Minerva",
        "Mitzy",
        "Miguel",
        "Miguel Ángel",
        "Miriam",
        "Modesto",
        "Mónica",
        "Nadia",
        "Natalia",
        "Natividad",
        "Nancy",
        "Nayeli",
        "Nelly",
        "Noelia",
        "Noemí",
        "Norma",
        "Nicolás",
        "Octavio",
        "Ofelia",
        "Olivia",
        "Óliver",
        "Olga",
        "Óscar",
        "Oswaldo",
        "Omar",
        "Pablo",
        "Paola",
        "Patricia",
        "Pamela",
        "Patricio",
        "Pascual",
        "Paulina",
        "Pedro",
        "Perla",
        "Pilar",
        "Porfirio",
        "Rafaél",
        "Ramiro",
        "Ramón",
        "Raúl",
        "Raquel",
        "Rebeca",
        "Reina",
        "Renato",
        "René",
        "Reynaldo",
        "Ricardo",
        "Roberto",
        "Rodolfo",
        "Rocío",
        "Rodrigo",
        "Rolando",
        "Rosa",
        "Rosalia",
        "Rosario",
        "Rubén",
        "Rufino",
        "Ruby",
        "Salvador",
        "Salma",
        "Samuel",
        "Sandra",
        "Santiago",
        "Sara",
        "Sessa",
        "Sergio",
        "Serafín",
        "Silvano",
        "Silvia",
        "Sofía",
        "Socorro",
        "Soledad",
        "Sonia",
        "Susana",
        "Tania",
        "Teresa",
        "Teodoro",
        "Timoteo",
        "Tomás",
        "Trinidad",
        "Verónica",
        "Vicente",
        "Violeta",
        "Uriel",
        "Úrsula",
        "Vanesa",
        "Víctor",
        "Victoria",
        "Virginia",
        "Wilfrido",
        "Wendolin",
        "Yeni",
        "Yolanda",
        "Yuridia",
        "Zacarías",
        "Zeferino",
        "Zoé",
    )

    last_names = (
        "Abrego",
        "Abreu",
        "Acevedo",
        "Acosta",
        "Acuña",
        "Adame",
        "Aguayo",
        "Aguilar",
        "Aguilera",
        "Aguirre",
        "Alarcón",
        "Alba",
        "Alcala",
        "Alcántar",
        "Alcaraz",
        "Alejandro",
        "Alemán",
        "Alfaro",
        "Almanza",
        "Almaraz",
        "Almonte",
        "Alonso",
        "Alonzo",
        "Altamirano",
        "Alva",
        "Alvarado",
        "Alvarez",
        "Amador",
        "Amaya",
        "Anaya",
        "Anguiano",
        "Angulo",
        "Aparicio",
        "Apodaca",
        "Aponte",
        "Aragón",
        "Aranda",
        "Arce",
        "Archuleta",
        "Arellano",
        "Arenas",
        "Arevalo",
        "Arguello",
        "Arias",
        "Armas",
        "Armendáriz",
        "Armenta",
        "Arredondo",
        "Arreola",
        "Arriaga",
        "Arroyo",
        "Arteaga",
        "Ávalos",
        "Ávila",
        "Avilés",
        "Ayala",
        "Baca",
        "Badillo",
        "Báez",
        "Baeza",
        "Bahena",
        "Balderas",
        "Ballesteros",
        "Bañuelos",
        "Barajas",
        "Barela",
        "Barragán",
        "Barraza",
        "Barrera",
        "Barreto",
        "Barrientos",
        "Barrios",
        "Batista",
        "Becerra",
        "Beltrán",
        "Benavides",
        "Benavídez",
        "Benítez",
        "Bermúdez",
        "Bernal",
        "Berríos",
        "Bétancourt",
        "Blanco",
        "Bonilla",
        "Borrego",
        "Botello",
        "Bravo",
        "Briones",
        "Briseño",
        "Brito",
        "Bueno",
        "Burgos",
        "Bustamante",
        "Bustos",
        "Caballero",
        "Cabán",
        "Cabrera",
        "Cadena",
        "Caldera",
        "Calderón",
        "Calvillo",
        "Camacho",
        "Camarillo",
        "Campos",
        "Canales",
        "Candelaria",
        "Cano",
        "Cantú",
        "Caraballo",
        "Carbajal",
        "Cardenas",
        "Cardona",
        "Carmona",
        "Carranza",
        "Carrasco",
        "Carreón",
        "Carrera",
        "Carrero",
        "Carrillo",
        "Carrión",
        "Carvajal",
        "Casanova",
        "Casares",
        "Casárez",
        "Casas",
        "Casillas",
        "Castañeda",
        "Castellanos",
        "Castillo",
        "Castro",
        "Cavazos",
        "Cazares",
        "Ceballos",
        "Cedillo",
        "Ceja",
        "Centeno",
        "Cepeda",
        "Cervantes",
        "Cervántez",
        "Chacón",
        "Chapa",
        "Chavarría",
        "Chávez",
        "Cintrón",
        "Cisneros",
        "Collado",
        "Collazo",
        "Colón",
        "Colunga",
        "Concepción",
        "Contreras",
        "Cordero",
        "Córdova",
        "Cornejo",
        "Corona",
        "Coronado",
        "Corral",
        "Corrales",
        "Correa",
        "Cortés",
        "Cortez",
        "Cotto",
        "Covarrubias",
        "Crespo",
        "Cruz",
        "Cuellar",
        "Curiel",
        "Dávila",
        "de Anda",
        "de Jesús",
        "de la Crúz",
        "de la Fuente",
        "de la Garza",
        "de la O",
        "de la Rosa",
        "de la Torre",
        "de León",
        "Delgadillo",
        "Delgado",
        "del Río",
        "del Valle",
        "Díaz",
        "Domínguez",
        "Duarte",
        "Dueñas",
        "Durán",
        "Echeverría",
        "Elizondo",
        "Enríquez",
        "Escalante",
        "Escamilla",
        "Escobar",
        "Escobedo",
        "Esparza",
        "Espinal",
        "Espino",
        "Espinosa",
        "Espinoza",
        "Esquibel",
        "Esquivel",
        "Estévez",
        "Estrada",
        "Fajardo",
        "Farías",
        "Feliciano",
        "Fernández",
        "Ferrer",
        "Fierro",
        "Figueroa",
        "Flores",
        "Flórez",
        "Fonseca",
        "Franco",
        "Frías",
        "Fuentes",
        "Gaitán",
        "Galarza",
        "Galindo",
        "Gallardo",
        "Gallegos",
        "Galván",
        "Gálvez",
        "Gamboa",
        "Gamez",
        "Gaona",
        "Garay",
        "García",
        "Garibay",
        "Garica",
        "Garrido",
        "Garza",
        "Gastélum",
        "Gaytán",
        "Gil",
        "Girón",
        "Godínez",
        "Godoy",
        "Gómez",
        "Gonzales",
        "González",
        "Gollum",
        "Gracia",
        "Granado",
        "Granados",
        "Griego",
        "Grijalva",
        "Guajardo",
        "Guardado",
        "Guerra",
        "Guerrero",
        "Guevara",
        "Guillen",
        "Gurule",
        "Gutiérrez",
        "Guzmán",
        "Haro",
        "Henríquez",
        "Heredia",
        "Hernádez",
        "Hernandes",
        "Hernández",
        "Herrera",
        "Hidalgo",
        "Hinojosa",
        "Holguín",
        "Huerta",
        "Hurtado",
        "Ibarra",
        "Iglesias",
        "Irizarry",
        "Jaime",
        "Jaimes",
        "Jáquez",
        "Jaramillo",
        "Jasso",
        "Jiménez",
        "Jimínez",
        "Juárez",
        "Jurado",
        "Laboy",
        "Lara",
        "Laureano",
        "Leal",
        "Lebrón",
        "Ledesma",
        "Leiva",
        "Lemus",
        "León",
        "Lerma",
        "Leyva",
        "Limón",
        "Linares",
        "Lira",
        "Llamas",
        "Loera",
        "Lomeli",
        "Longoria",
        "López",
        "Lovato",
        "Loya",
        "Lozada",
        "Lozano",
        "Lucero",
        "Lucio",
        "Luevano",
        "Lugo",
        "Luna",
        "Macías",
        "Madera",
        "Madrid",
        "Madrigal",
        "Maestas",
        "Magaña",
        "Malave",
        "Maldonado",
        "Manzanares",
        "Mares",
        "Marín",
        "Márquez",
        "Marrero",
        "Marroquín",
        "Martínez",
        "Mascareñas",
        "Mata",
        "Mateo",
        "Matías",
        "Matos",
        "Maya",
        "Mayorga",
        "Medina",
        "Medrano",
        "Mejía",
        "Meléndez",
        "Melgar",
        "Mena",
        "Menchaca",
        "Méndez",
        "Mendoza",
        "Menéndez",
        "Meraz",
        "Mercado",
        "Merino",
        "Mesa",
        "Meza",
        "Miramontes",
        "Miranda",
        "Mireles",
        "Mojica",
        "Molina",
        "Mondragón",
        "Monroy",
        "Montalvo",
        "Montañez",
        "Montaño",
        "Montemayor",
        "Montenegro",
        "Montero",
        "Montes",
        "Montez",
        "Montoya",
        "Mora",
        "Morales",
        "Moreno",
        "Mota",
        "Moya",
        "Munguía",
        "Muñiz",
        "Muñoz",
        "Murillo",
        "Muro",
        "Nájera",
        "Naranjo",
        "Narváez",
        "Nava",
        "Navarrete",
        "Navarro",
        "Nazario",
        "Negrete",
        "Negrón",
        "Nevárez",
        "Nieto",
        "Nieves",
        "Niño",
        "Noriega",
        "Núñez",
        "Ocampo",
        "Ocasio",
        "Ochoa",
        "Ojeda",
        "Olivares",
        "Olivárez",
        "Olivas",
        "Olivera",
        "Olivo",
        "Olmos",
        "Olvera",
        "Ontiveros",
        "Oquendo",
        "Ordóñez",
        "Orellana",
        "Ornelas",
        "Orosco",
        "Orozco",
        "Orta",
        "Ortega",
        "Ortiz",
        "Osorio",
        "Otero",
        "Ozuna",
        "Pabón",
        "Pacheco",
        "Padilla",
        "Padrón",
        "Páez",
        "Palacios",
        "Palomino",
        "Palomo",
        "Pantoja",
        "Paredes",
        "Parra",
        "Partida",
        "Patiño",
        "Paz",
        "Pedraza",
        "Pedroza",
        "Pelayo",
        "Peña",
        "Perales",
        "Peralta",
        "Perea",
        "Peres",
        "Pérez",
        "Pichardo",
        "Piña",
        "Pineda",
        "Pizarro",
        "Polanco",
        "Ponce",
        "Porras",
        "Portillo",
        "Posada",
        "Prado",
        "Preciado",
        "Prieto",
        "Puente",
        "Puga",
        "Pulido",
        "Quesada",
        "Quezada",
        "Quiñones",
        "Quiñónez",
        "Quintana",
        "Quintanilla",
        "Quintero",
        "Quiroz",
        "Rael",
        "Ramírez",
        "Ramón",
        "Ramos",
        "Rangel",
        "Rascón",
        "Raya",
        "Razo",
        "Regalado",
        "Rendón",
        "Rentería",
        "Reséndez",
        "Reyes",
        "Reyna",
        "Reynoso",
        "Rico",
        "Rincón",
        "Riojas",
        "Ríos",
        "Rivas",
        "Rivera",
        "Rivero",
        "Robledo",
        "Robles",
        "Rocha",
        "Rodarte",
        "Rodrígez",
        "Rodríguez",
        "Rodríquez",
        "Rojas",
        "Rojo",
        "Roldán",
        "Rolón",
        "Romero",
        "Romo",
        "Roque",
        "Rosado",
        "Rosales",
        "Rosario",
        "Rosas",
        "Roybal",
        "Rubio",
        "Ruelas",
        "Ruiz",
        "Saavedra",
        "Sáenz",
        "Saiz",
        "Salas",
        "Salazar",
        "Salcedo",
        "Salcido",
        "Saldaña",
        "Saldivar",
        "Salgado",
        "Salinas",
        "Samaniego",
        "Sanabria",
        "Sanches",
        "Sánchez",
        "Sandoval",
        "Santacruz",
        "Santana",
        "Santiago",
        "Santillán",
        "Sarabia",
        "Sauceda",
        "Saucedo",
        "Segovia",
        "Segura",
        "Sepúlveda",
        "Serna",
        "Serrano",
        "Serrato",
        "Sevilla",
        "Sierra",
        "Sisneros",
        "Solano",
        "Solís",
        "Soliz",
        "Solorio",
        "Solorzano",
        "Soria",
        "Sosa",
        "Sotelo",
        "Soto",
        "Suárez",
        "Tafoya",
        "Tamayo",
        "Tamez",
        "Tapia",
        "Tejada",
        "Tejeda",
        "Téllez",
        "Tello",
        "Terán",
        "Terrazas",
        "Tijerina",
        "Tirado",
        "Toledo",
        "Toro",
        "Torres",
        "Tórrez",
        "Tovar",
        "Trejo",
        "Treviño",
        "Trujillo",
        "Ulibarri",
        "Ulloa",
        "Urbina",
        "Ureña",
        "Urías",
        "Uribe",
        "Urrutia",
        "Vaca",
        "Valadez",
        "Valdés",
        "Valdez",
        "Valdivia",
        "Valencia",
        "Valentín",
        "Valenzuela",
        "Valladares",
        "Valle",
        "Vallejo",
        "Valles",
        "Valverde",
        "Vanegas",
        "Varela",
        "Vargas",
        "Vásquez",
        "Vázquez",
        "Vega",
        "Vela",
        "Velasco",
        "Velásquez",
        "Velázquez",
        "Vélez",
        "Véliz",
        "Venegas",
        "Vera",
        "Verdugo",
        "Verduzco",
        "Vergara",
        "Viera",
        "Vigil",
        "Villa",
        "Villagómez",
        "Villalobos",
        "Villalpando",
        "Villanueva",
        "Villareal",
        "Villarreal",
        "Villaseñor",
        "Villegas",
        "Yáñez",
        "Ybarra",
        "Zambrano",
        "Zamora",
        "Zamudio",
        "Zapata",
        "Zaragoza",
        "Zarate",
        "Zavala",
        "Zayas",
        "Zedillo",
        "Zelaya",
        "Zepeda",
        "Zúñiga",
    )

    prefixes = ("Sr(a).", "Dr.", "Mtro.", "Lic.", "Ing.")
