
import os
import requests
import time
from plyer import notification

#Installer pip request via à votre terminal si ce n'est pas déjà le cas
#pip install requests
#python.exe -m pip install --upgrade pip

#Pour placer la clé API vous devez dans informations systeme > parametre avancé
#> variable d'environement placer votre clé API et bien la nomé "COIN_API"

alert = int
rAlert = []
gAlert = []
scd = 60

cle_api = os.environ.get('COIN_API')
assert cle_api != None

def envoyer_alerte_display(message):
    notification.notify(
        title='Alerte Bitcoin',
        message=message,
        app_name='Python Bitcoin Alert',
        timeout=10  
    )

def obtenir_cours_bitcoin(api_key):
    url_api = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    headers = {
        'X-CoinAPI-Key': api_key
    }

    try:
        reponse = requests.get(url_api, headers=headers)
        reponse.raise_for_status()  # Lève une exception pour les erreurs HTTP
        donnees = reponse.json()
        cours_bitcoin = donnees['rate']
        return cours_bitcoin
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête API : {e}")
        return None

def surveiller_cours_bitcoin(api_key, gAlert, rAlert, scd):
    while True:
        cours_actuel = obtenir_cours_bitcoin(api_key)

        if cours_actuel is not None:
            print(f"Le cours actuel du Bitcoin est de {cours_actuel} USD.")
            for i in range(len(gAlert)):
                if cours_actuel > gAlert[i]:
                    message_alerte = f"ALERT: Le cours du Bitcoin a dépassé le seuil d'alerte de {gAlert[i]} USD!"
                    print(message_alerte)
                    envoyer_alerte_display(message_alerte)
            
            for i in range(len(rAlert)):
                if cours_actuel < rAlert[i]:
                    message_alerte = f"ALERT: Le cours du Bitcoin a dépassé le sol d'alerte de {rAlert[i]} USD!"
                    print(message_alerte)
                    envoyer_alerte_display(message_alerte)
                
        time.sleep(scd) 



choice = str
while choice != " ":
    
    print("\nListe des alertes:\n\n Seuil haut")
    for i in range (len(rAlert)):
        print("\n"+ str(i + 1) + ":" + str(rAlert[i]) + " USD")
        
    print("\n Seuil bas")    
    for i in range (len(gAlert)):
        print("\n"+ str(i + 1 + len(rAlert)) + ":" + str(gAlert[i]) + "USD")
    
    print("\n\"r\": Ajouter un seuil du bas\n\"g\": Ajouter un seuil du haut\n\"d\": supprimer un seuil\n\"u\": moiffier un seuil\n\"touche espace\": Pour commencer le programme\n\"t\": Pour commencer le programme")
    
    choice = str(input("\nChoisir action\n"))
    
    if choice == 'r' or choice == 'R':
        alert = int(input("\nA combien se trouve le seuil"))
        if alert > 0 :
            rAlert.append(alert)
        else: 
            print("\nVous n'avez pas choisis un entier positif")
            continue   
    
    if choice == 'g' or choice == 'G':
        alert = int(input("\nA combien se trouve le seuil"))
        if alert > 0 :
            gAlert.append(alert)
        else:
            print("\nVous n'avez pas choisis un entier positif")
            continue   
        
    if choice == 'd' or choice == 'D':
        i = int(input('\nQuel alert supprimer ?'))
        if i < 0 and i < len(rAlert) - 1:
            i = i - 1
            del rAlert[i]
        elif i > len(rAlert) - 1:
            i = i - len(rAlert) - 1
            print(i)
            del gAlert[i]
        else:
            print("\nIl y a une erreur !")
            continue
    
    if choice == 'u' or choice == 'U':
        i = int(input('\nQuel alert modifier ?'))
        v = int(input("\nPar quelle valeur ?"))
        if v > 0:
            if i < 0 and i < len(rAlert) - 1:
                i = i - 1
                rAlert[i] = v
            elif i > len(rAlert) - 1:
                i = i - len(rAlert) - 1
                gAlert[i] = v
            else:
                print("\nIl y a une erreur !")
                continue  
            
    if choice == 't' or choice == 'T':
        scd = int(input("Combien de seconde entre chaques vérifications ?"))

surveiller_cours_bitcoin(cle_api, gAlert, rAlert, scd)
