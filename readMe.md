**README**

[N° 010 : BOTTICELLI_BOT](#_Toc181870652)

[N° 020 : traiterISAD_BOT](#_Toc181870653)

[N° 030 : comparerISADetISAAR_BOT](#_Toc181870654)

[N°040 : Fichier ABES ; N°050_VERIFICATIONS DES ALIGNEMENTS : étapes manuelles, notamment de vérification des alignements des résultats trouvés sur IdRef](#_Toc181870655)

[N° 060 : reunirPhoebusIdRef_BOT](#_Toc181870656)

[N° 070 : ENVOI A IDREF : dossier de stockage des fichiers csv envoyés à IdRef](#_Toc181870657)

[N°80 : SKYSCRAPER_BOT](#_Toc181870658)

[N° 090 : BOTORITE-2-0](#_Toc181870659)

[N°100 : CROWDSOURCER](#_Toc181870660)

[Crédits](#_Toc181870661)

[Conditions d'utilisation](#_Toc181870662)

N° 010 : BOTTICELLI_BOT
-----------------------

**Description**

Ce script permet de parcourir et d'analyser des données sur la plateforme AtoM pour des documents d'archives du Centre des littératures en Suisse romande de l'université de Lausanne. Le script utilise plusieurs bibliothèques pour automatiser la navigation sur AtoM, extraire des données, identifier des noms pertinents dans les correspondances, les comparer à une liste de noms d'autorité, puis indexer automatiquement les résultats sur la plateforme.

**Fonctionnalités principales :**

1.  **Connexion à AtoM** : Automatisation de l'ouverture de session à l'aide de la bibliothèque webbot.
2.  **Navigation et Extraction de Données** : Accès aux pages de recherche et collecte des informations sur les correspondances.
3.  **Détection de Noms** : Extraction des noms de personnes dans les titres, avec déduplication.
4.  **Comparaison avec des Notions d'Autorité** : Comparaison des noms extraits avec une liste de noms d'autorité.
5.  **Indexation Automatique** : Ajout des noms d'autorité trouvés dans les champs d'indexation d'AtoM pour chaque document correspondant.

**Installation**

Assurez-vous d'installer les dépendances Python nécessaires :

pip install webbot beautifulsoup4 numpy pandas spacy flair networkx python-Levenshtein unidecode seaborn matplotlib

Le script dépend d'un fichier credentials.json contenant les identifiants pour accéder à la plateforme AtoM :

{

    "email": "votre_email",

    "password": "votre_mot_de_passe"

}

**Utilisation**

1.  **Connexion** : Le script commence par ouvrir AtoM et se connecte avec les identifiants.
2.  **Extraction des Correspondances** : Il collecte les données de correspondance et les noms d'acteurs.
3.  **Comparaison et Nettoyage des Noms** : Les noms trouvés sont comparés aux noms d'autorité et dédoublonnés.
4.  **Indexation sur AtoM** : Le script automatise l'ajout de noms d'autorité aux archives.

**Avertissement**

-   Ce script effectue de nombreuses actions automatisées ; il est important de respecter les politiques d'utilisation d'AtoM.
-   Utilisez un délai (sleep) entre chaque requête pour éviter de surcharger le serveur.

N° 020 : traiterISAD_BOT
------------------------

**Description**

Ce script Python compare les autorités contenues dans des fichiers CSV avec celles extraites de Phoebus (AtoM) et identifie les notices incomplètes ou non alignées. Il génère un nouveau fichier CSV à partir des données sources, indiquant l'état de chaque autorité (à réexaminer ou complète) et ajoutant des informations supplémentaires, si disponible.

**Fonctionnalités**

-   Compare les autorités présentes dans un fichier d'anciennes autorités (old_authority_csv_file) avec des fichiers de notices ISAAR-CPF extraites de Phoebus.
-   Recherche les autorités ayant un statut "Ébauche", "Non aligné" ou vide dans la base de données.
-   Ajoute des colonnes d'informations supplémentaires (dates d'existence, historique, identifiant) dans le fichier de sortie si l'autorité est incomplète.
-   Génère un fichier CSV indiquant l'état du traitement de chaque autorité ("A REEXAMINER" ou "AUTORITE COMPLETE").

**Prérequis**

-   Python 3.x
-   Bibliothèque csv

**Utilisation**

**Étape 1: Comparaison et extraction**

1.  Préparez vos fichiers CSV :

-   old_authority_csv_file : Fichier contenant les anciennes autorités.
-   input_csv_files : Liste des fichiers CSV contenant les notices ISAAR extraites de Phoebus.
-   output_csv_file : Nom du fichier CSV généré avec l'état de chaque autorité.

3.  Exécutez le script avec les chemins de vos fichiers comme paramètres.

python

find_matching_authorities(old_authority_csv_file, input_csv_files, output_csv_file)

**Sortie**

Le script génère un fichier CSV avec les informations suivantes :

-   Etat du traitement : Indique si l'autorité doit être réexaminée ou si elle est complète.
-   ISAAR_datesOfExistence, ISAAR_history, ISAAR_identifiant : Ajoute des informations supplémentaires sur les autorités trouvées et incomplètes.

**Note**

Les fichiers CSV doivent être bien structurés et utiliser les colonnes suivantes :

-   nameAccessPoints (pour les anciennes autorités),
-   authorizedFormOfName, status, datesOfExistence, history, descriptionIdentifier (pour les fichiers de notices ISAAR).

N° 030 : comparerISADetISAAR_BOT
--------------------------------

**Description**

Ce script a pour but de comparer les autorités présentes dans différents fichiers CSV. Il identifie les autorités présentes dans Phoebus mais non encore alignées avec IdRef (statut "Ébauche", "Non aligné" ou sans statut), et génère un fichier CSV de sortie indiquant les autorités à réexaminer. Ce fichier de sortie contient également des informations supplémentaires de type ISAAR (comme les dates d'existence, l'historique et un identifiant).

**Fonctionnalités**

-   **Comparaison d'autorités** : Le script compare les noms dans le fichier principal des autorités (Phoebus) avec les autorités dans des fichiers CSV d'entrée.
-   **Filtrage par statut** : Il identifie les autorités dont le statut est "Ébauche", "Non aligné" ou vide, indiquant qu'elles sont présentes dans Phoebus mais non alignées avec IdRef.
-   **Extraction de données supplémentaires** : Le script récupère et ajoute des informations additionnelles, telles que les dates d'existence, l'historique, et un identifiant, pour chaque autorité trouvée.
-   **Écriture dans un fichier de sortie** : Les autorités incomplètes sont étiquetées comme "A REEXAMINER" dans un fichier de sortie, tandis que les autorités complètes sont étiquetées "AUTORITE COMPLETE".

**Pré-requis**

-   **Python 3.x**
-   **Bibliothèque standard csv** : Aucune installation supplémentaire n'est requise pour exécuter le script.

**Utilisation**

1.  **Fichiers nécessaires** :

-   Un fichier CSV principal contenant les autorités, par exemple 03_isad_data_OUTPUT.csv.
-   Plusieurs fichiers CSV d'entrée avec les informations ISAAR (extraits de Phoebus) dans un dossier, comme noticesAutorite_2024-06-10/.

3.  **Paramétrage des chemins** :

-   Dans le code, spécifiez les chemins des fichiers d'entrée (old_authority_csv_file et input_csv_files) et du fichier de sortie (output_csv_file).

5.  **Exécution du script** :

-   Exécutez le script en appelant la fonction find_matching_authorities() avec les chemins appropriés.

**Structure du fichier de sortie**

Le fichier de sortie, nommé autoritesAReexaminerISAD_ISAAR.csv, inclut les colonnes suivantes :

-   **Les colonnes d'origine** du fichier des autorités Phoebus.
-   **Etat du traitement** : Indique si l'autorité est "A REEXAMINER" (incomplète) ou "AUTORITE COMPLETE".
-   **ISAAR_datesOfExistence** : Les dates d'existence récupérées.
-   **ISAAR_history** : L'historique de l'autorité.
-   **ISAAR_identifiant** : L'identifiant de l'autorité.

N°040 : Fichier ABES ; N°050_VERIFICATIONS DES ALIGNEMENTS : étapes manuelles, notamment de vérification des alignements des résultats trouvés sur IdRef
--------------------------------------------------------------------------------------------------------------------------------------------------------

N° 060 : reunirPhoebusIdRef_BOT
-------------------------------

**Description**

Ce script automatise la récupération de données depuis la plateforme Phoebus. Il permet de se connecter à la plateforme, d'effectuer des recherches d'autorités, et de récupérer les liens vers les notices d'autorité. Les résultats sont ensuite enregistrés dans des fichiers CSV pour une gestion ultérieure. Le processus comporte plusieurs étapes, allant de la connexion à Phoebus à l'exportation des résultats vers un fichier CSV.

**Prérequis**

Avant d'exécuter ce script, assurez-vous que vous avez installé les dépendances suivantes :

-   requests : Pour effectuer les requêtes HTTP.
-   beautifulsoup4 : Pour analyser le contenu HTML.
-   pandas : Pour traiter les fichiers CSV.
-   webbot : Pour automatiser la navigation avec un navigateur.
-   json : Pour charger les informations de connexion.

Vous pouvez installer ces bibliothèques avec la commande suivante :

pip install requests beautifulsoup4 pandas webbot

**Étapes du processus**

**1\. Connexion à la plateforme Phoebus**

La fonction access_atom() se connecte automatiquement à la plateforme Phoebus en utilisant les identifiants stockés dans un fichier credentials.json. Le fichier doit contenir les champs suivants :

-   email: Votre adresse email pour vous connecter.
-   password: Votre mot de passe.

**2\. Extraction des autorités depuis un fichier CSV**

La fonction extract_autoritePhoebus() extrait les autorités à partir d'un fichier CSV spécifié (01_autorite.csv). Ces données sont stockées dans une liste pour être utilisées dans les étapes suivantes.

**3\. Construction des URL de recherche**

La fonction search_autoritie() génère des URL de recherche pour chaque autorité dans Phoebus. Ces URL sont ensuite utilisées pour récupérer les résultats.

**4\. Récupération des notices d'autorité**

La fonction browse_autorites() parcourt chaque URL de recherche et extrait les liens vers les notices d'autorité correspondantes. Les résultats sont enregistrés dans une liste.

**5\. Export des résultats dans un fichier CSV**

La fonction write_to_csv() crée un fichier CSV (02_autoritiesOnPhoebus.csv) qui contient le nom de l'autorité, le nombre de notices trouvées, et les liens vers les notices d'autorité correspondantes.

**6\. Contrôle humain**

Après avoir exporté les résultats dans un CSV, vous devez vérifier les données et ajuster manuellement les résultats multiples et les erreurs éventuelles.

**7\. Extraction des URLs nettoyées**

La fonction extract_hrefs_list_cleaned() extrait les liens vers les notices valides depuis le fichier CSV nettoyé (02_autoritiesOnPhoebus.csv).

**8\. Exportation vers un fichier final**

La fonction two_columns_csv() crée un fichier CSV final (03_phoebusEtIdRef.csv) contenant les URLs vers Phoebus et les identifiants IdRef correspondants.

**9\. Vérification des fichiers CSV**

La fonction compare_nb_lignes_csv() compare le nombre de lignes des trois fichiers CSV pour s'assurer qu'ils sont cohérents.

**Structure du projet**

├── 01_autorite.csv        # Fichier CSV avec les autorités à rechercher

├── 02_autoritiesOnPhoebus.csv  # Résultats de la recherche dans Phoebus

├── 03_phoebusEtIdRef.csv  # Fichier final avec les URLs et les IdRef

├── credentials.json       # Fichier contenant les identifiants de connexion

**Instructions d'utilisation**

1.  Créez un fichier credentials.json contenant votre adresse email et votre mot de passe pour la connexion à Phoebus.
2.  Placez votre fichier CSV initial (01_autorite.csv) avec les autorités à rechercher.
3.  Exécutez le script Python. Chaque étape sera effectuée automatiquement :

-   Connexion à Phoebus
-   Recherche des autorités
-   Récupération des notices d'autorité
-   Export des résultats dans des fichiers CSV.

5.  Vérifiez et ajustez manuellement les résultats si nécessaire.
6.  Exécutez la fonction finale pour générer le fichier CSV avec les données nettoyées et prêtes à être utilisées.

**Exemple de Résultat**

**Exemple de ****02_autoritiesOnPhoebus.csv**

|

**authorizedFormOfName**

 |

**nbre de notices**

 |

**notice 1**

 |

**notice 2**

 |

**notice 3**

 |
| --- | --- | --- | --- | --- |
|

Jean Dupont

 |

2

 |

link1

 |

link2

 |

NULL

 |
|

Marie Curie

 |

1

 |

link3

 |

NULL

 |

NULL

 |

**Exemple de ****03_phoebusEtIdRef.csv**

|

**authorizedFormOfName**

 |

**url_phoebus**

 |

**Sources**

 |
| --- | --- | --- |
|

Jean Dupont

 |

link1

 |

IdRef1

 |
|

Marie Curie

 |

link3

 |

IdRef2

 |

N° 070 : ENVOI A IDREF : dossier de stockage des fichiers csv envoyés à IdRef
-----------------------------------------------------------------------------

N°80 : SKYSCRAPER_BOT
---------------------

**Description**

Ce script effectue l'extraction de données d'autorité depuis des fichiers CSV et des ressources en ligne (Phoebus et IDRef), en les enrichissant avec des informations XML associées. Il est conçu pour automatiser le processus de récupération d'informations et gérer les erreurs réseau grâce à une gestion avancée des erreurs de connexion et des timeouts.

Le script est structuré en deux étapes principales :

Extraction de données à partir d'un fichier CSV - Récupère des URL et des informations d'autorité à partir de fichiers CSV.

Collecte des informations sur IDRef - Envoie des requêtes HTTP pour extraire les informations des notices XML d'IDRef en utilisant la bibliothèque BeautifulSoup pour analyser les données XML.

**Prérequis**

Python 3.x

Packages Python nécessaires :

pandas : pour manipuler les données CSV

requests : pour gérer les requêtes HTTP

BeautifulSoup (via bs4) : pour analyser le contenu XML

urllib et webbrowser : pour la manipulation d'URL et l'ouverture de liens (optionnel)

datetime et time : pour gérer et formater les dates de création/modification et les délais entre les requêtes.

**Utilisation**

**Configurer les paramètres du fichier CSV :**

Définir le chemin d'accès au fichier CSV contenant les données.

Indiquer les noms des colonnes pour les URL Phoebus et les liens IdRef.

**Lancer les fonctions :**

Utilisez les fonctions extract_autorite() et extract_idRef() pour extraire les URL des notices d'autorité et les informations d'IDRef à partir du fichier CSV.

extract_from_idRef() récupère les données XML d'IDRef, les analyse, et les structure pour l'export.

**Structure du Code**

-   **En-têtes HTTP **: Les en-têtes sont configurés pour simuler une requête venant d'un navigateur, afin d'assurer l'accès aux données.
-   **Étape 1 : Acquisition des données :**

-   extract_autorite() : Extrait les URLs de recherche Phoebus depuis un fichier CSV.
-   extract_idRef() : Extrait les URLs IDRef, les convertit en format XML, et retourne une liste d'URLs XML.

-   **Étape 2 : Récupération des données depuis IDRef :**

-   extract_from_idRef() : Envoie des requêtes pour chaque URL IDRef, extrait et formate les informations de la notice, incluant :

-   Nom et prénom autorisés : Extrait les noms et prénoms standards.
-   Dates d'existence : Récupère les années de naissance et décès (ou période approximative).
-   Fonctions : Rôle ou fonction associé à l'entité.
-   Note publique : Informations complémentaires sur l'entité.
-   Historique et biographies : Informations biographiques supplémentaires.
-   Autres formes de noms : Noms alternatifs ou surnoms.
-   Références et métadonnées : URI IDRef, date de création et de modification de la notice.

-   **Formatage des données :**

-   Supprime les espaces en trop, unifie les valeurs NULL, et normalise la mise en forme.

-   **Sortie : **Les informations extraites sont sauvegardées dans un fichier CSV.

**Résultats**

Le script génère un fichier CSV contenant les colonnes suivantes pour chaque notice :

-   Nom autorisé : Forme standard du nom, en majuscules.
-   Prénom autorisé : Forme standard du prénom.
-   Dates d'existence : Période de vie de l'entité.
-   Fonctions : Fonctions exercées par l'entité (ex. "historien", "écrivain").
-   Note publique : Informations complémentaires sous forme de note.
-   Historique : Informations biographiques et note publique combinées pour constituer un historique complet.
-   Autres formes de noms : Noms alternatifs sous lesquels l'entité est connue.
-   URI : Lien vers la page IDRef de la notice d'autorité.
-   Dates de création et de modification : Informations sur la création et la dernière révision de la notice.

N° 090 : BOTORITE-2-0
---------------------

**Description**

Ce script utilise l'automatisation pour accéder à la plateforme Phoebus, récupérer des données depuis un fichier CSV, naviguer dans des pages de notices d'autorité, et saisir automatiquement des informations dans les champs appropriés des notices. Il utilise Selenium, BeautifulSoup, et la bibliothèque webbot pour interagir avec l'interface web et remplir les champs de manière automatisée.

**Prérequis**

Avant d'exécuter ce script, assurez-vous que vous avez installé les bibliothèques suivantes :

-   Python 3.x
-   webbot
-   selenium
-   pandas
-   requests
-   beautifulsoup4
-   unidecode

**Utilisation**

1.  **Configuration des identifiants** :

-   Créez un fichier credentials.json dans le même répertoire que le script, avec la structure suivante pour stocker vos identifiants Phoebus

3.  **Lancement du Script** :

-   Dans un terminal, exécutez le script Python. Les étapes suivantes seront réalisées :

-   **Connexion** à la plateforme Phoebus
-   **Extraction des données** d'autorité à partir d'un fichier CSV (comme 01_noticesACompleter.csv)
-   **Accès aux notices** en mode édition pour chacune des URL générées
-   **Saisie automatisée** des informations dans les champs des notices d'autorité.

5.  **Vérification des résultats** :

-   Le script affiche des messages de confirmation pour chaque étape réussie et indique toute erreur rencontrée pour faciliter le débogage.

**Structure**

Le script est divisé en plusieurs étapes fonctionnelles :

-   **Étape 1 : access_atom(driver)**

-   Cette fonction ouvre une session sur la plateforme Phoebus en utilisant les identifiants présents dans le fichier credentials.json.

-   **Étape 2 : extract_autorite(csv_path)**

-   Extrait les noms et données d'autorité depuis un fichier CSV spécifié.

-   **Étape 3 : open_autorites(csv_path)**

-   Ajoute un suffixe à chaque URL d'autorité pour accéder directement aux pages en mode édition.

-   **Étape 4 : modify_autorites(driver, autorities, autorites_url)**

-   Ouvre chaque notice en mode édition, remplit les champs d'information, et sauvegarde les modifications.

**Résultats**

À l'exécution, ce script génère les résultats suivants :

-   **Connexion automatisée** : Ouverture de session sur la plateforme Phoebus avec les identifiants fournis.
-   **Extraction et affichage des données d'autorité** : Vérification des autorités extraites depuis le CSV pour confirmer leur exactitude.
-   **Modification des notices** : Remplissage automatique des champs des notices avec les informations appropriées et affichage d'un message de réussite ou d'erreur pour chaque saisie.
-   **Sauvegarde des modifications** : Confirmation que les modifications ont été sauvegardées avec succès pour chaque notice traitée.

En cas d'erreur, le script affiche le message correspondant à l'erreur rencontrée, facilitant ainsi la gestion et la correction de problèmes.

**Note** : les script BOTORITE_enrichissement IDREF et BOTORITE_renvoi vers IDREF sont identique, excepté le texte rédigé dans le champ « Sources » d'AtoM. Le premier est destiné aux notices qui ont bénéficié des informations extraites d'IdRef et le second s'applique aux notices qui nécessite qu'un simple renvoi vers IdRef.

Dans les deux cas, les notices AtoM et IdRef sont liées par une lien url.

N°100 : CROWDSOURCER
--------------------

**Description**

Ce script permet de traiter les notices qui n'ont pas été alignées avec IdRef, et est structuré en deux parties, la première permet de récupère les URLs des notices Phoebus, la deuxième permet de les saisir automatiquement dans AtoM.

**ETAPE_1_urlPHOEBUS**

**Prérequis**

Le script s'appuie sur les bibliothèques Python suivantes :

- pandas: pour manipuler et lire le fichier CSV contenant les noms d'autorité.

- requests: pour effectuer des requêtes HTTP et récupérer les pages de résultats.

- BeautifulSoup: pour analyser et extraire des données à partir de pages HTML.

- webbot: pour automatiser la connexion à Phoebus.

- csv: pour l'écriture des résultats dans un fichier CSV.

- datetime et time: pour la gestion du temps dans les requêtes.

**Structure**

ETAPE 1 : Connexion à Atom

La fonction access_atom(driver) utilise webbot pour ouvrir la page de connexion de Phoebus, et se connecter avec les identifiants stockés dans un fichier credentials.json.

ETAPE 2 : Extraction des données d'autorité

La fonction extract_autoritePhoebus(csv_path) lit un fichier CSV d'entrée contenant les noms d'autorité et les retourne sous forme de liste.

ETAPE 3 : Construction de l'URL de recherche

La fonction search_autoritie(autorities_list) construit les URLs de recherche pour chaque nom et les visite via webbot.

ETAPE 4 : Récupération des liens d'édition

La fonction browse_autorites(search_urls) récupère les liens vers les notices d'autorité depuis les pages de résultats.

ETAPE 5 : Création d'un fichier CSV de gestion des résultats

La fonction write_to_csv(hrefs_list, autorities) écrit les noms d'autorité et les liens récupérés dans un fichier CSV, en ajoutant une colonne pour le nombre de notices trouvées.

ETAPE 6 : Contrôle humain des résultats

À la fin de l'exécution, effectuez un contrôle manuel pour :

Vérifier les lignes avec 0 résultats, pour confirmer l'absence de notices correspondantes.

En cas de résultats multiples, sélectionner le bon et le coller dans la colonne appropriée du CSV.

**Etape_2 _BOTORITE_ebauche**

**Prérequis**

Voir BOTORITE 2-0

**Structure**

Voir BOTORITE 2-0

**Note : **le script fonctionne comme botorité 2.0, excepté dans le champ « Contenu » d'AtoM, où s'inscrit une mention de crowdsourcing.

Crédits
-------

- **Auteur de BOTTICELLI_**BOT et botorité: Amin Mekacher

- **Auteur des autres scripts** : Nam Pham, avec l'aide de ChatGPT 3-5

- **Date** : 2021 ; 2023-2024

Conditions d'utilisation
------------------------

Ce travail est mis à disposition selon les termes de la licence [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Cela signifie que vous pouvez :

- Partager, copier, distribuer et transmettre le travail, à condition de citer l'auteur.

- Créer des œuvres dérivées, tant que vous donnez également crédit à l'auteur et que vous ne les utilisez pas à des fins commerciales, selon les conditions de la licence.