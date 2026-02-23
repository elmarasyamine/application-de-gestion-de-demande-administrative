"""
Actions custom pour le chatbot Rasa.
Ces actions appellent l'API Spring Boot (http://localhost:8093) pour recuperer
les donnees reelles des demandes depuis la base de donnees MySQL.
"""

import requests
import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# URL de base de l'API Spring Boot
SPRING_BOOT_API = "http://localhost:8093/api"


class ActionVoirDemandes(Action):
    """
    Action pour recuperer toutes les demandes d'un utilisateur
    depuis l'API Spring Boot.
    """

    def name(self) -> Text:
        return "action_voir_demandes"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Recuperer le user_id depuis les metadonnees ou le slot
        user_id = tracker.get_slot("user_id")

        if not user_id:
            metadata = tracker.latest_message.get("metadata", {})
            user_id = metadata.get("userId") or metadata.get("user_id")

        if not user_id:
            dispatcher.utter_message(
                text="Vous devez etre connecte pour consulter vos demandes. Rendez-vous sur la page de connexion.",
                buttons=[
                    {"title": "Comment se connecter ?", "payload": "/faq_connexion"},
                    {"title": "Aide", "payload": "/demander_aide"},
                ],
            )
            return []

        try:
            response = requests.get(
                f"{SPRING_BOOT_API}/demandes/mes-demandes/{user_id}",
                timeout=10,
            )

            if response.status_code == 200:
                demandes = response.json()

                if not demandes:
                    dispatcher.utter_message(
                        text="Vous n'avez aucune demande pour le moment.\n\nSouhaitez-vous en soumettre une ?",
                        buttons=[
                            {
                                "title": "Soumettre une demande",
                                "payload": "/soumettre_demande",
                            },
                            {
                                "title": "Types de demandes",
                                "payload": "/types_demandes",
                            },
                            {"title": "Aide", "payload": "/demander_aide"},
                        ],
                    )
                    return []

                # Construire le message avec les demandes
                msg = f"Vos demandes ({len(demandes)}) :\n\n"

                # Compteurs par statut
                stats = {"SOUMISE": 0, "EN_TRAITEMENT": 0, "VALIDEE": 0, "REJETEE": 0}

                for d in demandes:
                    ref = d.get("reference", "N/A")
                    titre = d.get("titreDemande", "Sans titre")
                    type_dem = d.get("typeDemande", "N/A")
                    status = d.get("status", "N/A")
                    status_display = self._format_status(status)
                    status_icon = self._status_icon(status)
                    date = d.get("dateDepot", "")

                    if status in stats:
                        stats[status] += 1

                    msg += f"{status_icon} {ref} - {titre}\n"
                    msg += f"   Type: {type_dem} | Statut: {status_display}"
                    if date:
                        msg += f" | Date: {date[:10]}"
                    msg += "\n\n"

                # Resume
                resume = "Resume : "
                parts = []
                if stats["SOUMISE"] > 0:
                    parts.append(f"{stats['SOUMISE']} soumise(s)")
                if stats["EN_TRAITEMENT"] > 0:
                    parts.append(f"{stats['EN_TRAITEMENT']} en traitement")
                if stats["VALIDEE"] > 0:
                    parts.append(f"{stats['VALIDEE']} validee(s)")
                if stats["REJETEE"] > 0:
                    parts.append(f"{stats['REJETEE']} rejetee(s)")
                if parts:
                    msg += resume + " | ".join(parts) + "\n\n"

                msg += "Tapez une reference (ex: REF-12345) pour plus de details."

                dispatcher.utter_message(
                    text=msg,
                    buttons=[
                        {
                            "title": "Soumettre une demande",
                            "payload": "/soumettre_demande",
                        },
                        {
                            "title": "Comprendre les statuts",
                            "payload": "/faq_statut_demande",
                        },
                        {
                            "title": "Delais de traitement",
                            "payload": "/delais_traitement",
                        },
                        {"title": "Aide", "payload": "/demander_aide"},
                    ],
                )
            else:
                dispatcher.utter_message(
                    text="Desole, je n'ai pas pu recuperer vos demandes. Veuillez reessayer plus tard.",
                    buttons=[
                        {"title": "Reessayer", "payload": "/voir_demandes"},
                        {"title": "Contact", "payload": "/contact"},
                        {"title": "Aide", "payload": "/demander_aide"},
                    ],
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Le serveur est temporairement indisponible. Veuillez reessayer dans quelques instants.",
                buttons=[
                    {"title": "Reessayer", "payload": "/voir_demandes"},
                    {"title": "Contact", "payload": "/contact"},
                ],
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"Une erreur est survenue : {str(e)}",
                buttons=[{"title": "Aide", "payload": "/demander_aide"}],
            )

        return []

    def _format_status(self, status: str) -> str:
        status_map = {
            "SOUMISE": "Soumise",
            "EN_TRAITEMENT": "En traitement",
            "VALIDEE": "Validee",
            "REJETEE": "Rejetee",
        }
        return status_map.get(status, status)

    def _status_icon(self, status: str) -> str:
        icon_map = {
            "SOUMISE": "[Soumise]",
            "EN_TRAITEMENT": "[En cours]",
            "VALIDEE": "[OK]",
            "REJETEE": "[Rejet]",
        }
        return icon_map.get(status, "[-]")


class ActionChercherReference(Action):
    """
    Action pour chercher une demande par sa reference
    depuis l'API Spring Boot.
    """

    def name(self) -> Text:
        return "action_chercher_reference"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Extraire la reference du message
        message = tracker.latest_message.get("text", "")
        reference = tracker.get_slot("reference")

        # Si pas de slot, essayer d'extraire depuis le message
        if not reference:
            ref_match = re.search(r"REF[- ]?(\d+)", message, re.IGNORECASE)
            if ref_match:
                reference = f"REF-{ref_match.group(1)}"

        if not reference:
            dispatcher.utter_message(
                text="Veuillez fournir une reference valide (format : REF-12345).\n\nVous pouvez trouver la reference dans la liste de vos demandes.",
                buttons=[
                    {
                        "title": "Voir mes demandes",
                        "payload": "/voir_demandes",
                    },
                    {"title": "Aide", "payload": "/demander_aide"},
                ],
            )
            return []

        # S'assurer que la reference est au bon format
        if not reference.upper().startswith("REF-"):
            reference = f"REF-{reference}"
        reference = reference.upper()

        try:
            response = requests.get(
                f"{SPRING_BOOT_API}/demandes/reference/{reference}",
                timeout=10,
            )

            if response.status_code == 200:
                d = response.json()

                status = d.get("status", "N/A")
                status_display = self._format_status(status)

                msg = f"Details de la demande {d.get('reference', reference)} :\n\n"
                msg += f"- Titre : {d.get('titreDemande', 'N/A')}\n"
                msg += f"- Type : {d.get('typeDemande', 'N/A')}\n"
                msg += f"- Statut : {status_display}\n"

                date = d.get("dateDepot", "")
                if date:
                    msg += f"- Date de depot : {date[:10]}\n"

                desc = d.get("description", "")
                if desc:
                    msg += f"- Description : {desc}\n"

                fichier = d.get("nomFichier", "")
                if fichier:
                    msg += f"- Fichier joint : {fichier}\n"

                # Conseils selon le statut
                msg += "\n"
                if status == "SOUMISE":
                    msg += "Votre demande est en attente d'assignation a un administrateur. Patience !"
                elif status == "EN_TRAITEMENT":
                    msg += "Un administrateur examine actuellement votre demande."
                elif status == "VALIDEE":
                    msg += "Votre demande a ete approuvee ! Vous pouvez telecharger le document dans vos demandes."
                elif status == "REJETEE":
                    msg += "Votre demande a ete rejetee. Contactez l'administration pour connaitre le motif."

                # Boutons contextuels
                buttons = [
                    {"title": "Voir toutes mes demandes", "payload": "/voir_demandes"},
                ]
                if status == "REJETEE":
                    buttons.append(
                        {"title": "Que faire apres un rejet ?", "payload": "/demande_rejetee"}
                    )
                    buttons.append(
                        {"title": "Soumettre nouvelle demande", "payload": "/soumettre_demande"}
                    )
                elif status == "VALIDEE":
                    buttons.append(
                        {"title": "Comment telecharger ?", "payload": "/faq_telecharger_document"}
                    )
                else:
                    buttons.append(
                        {"title": "Delais de traitement", "payload": "/delais_traitement"}
                    )
                buttons.append({"title": "Aide", "payload": "/demander_aide"})

                dispatcher.utter_message(text=msg, buttons=buttons)

            elif response.status_code == 404:
                dispatcher.utter_message(
                    text=f"Aucune demande trouvee avec la reference {reference}.\n\nVerifiez la reference et reessayez. Le format est : REF-XXXXX",
                    buttons=[
                        {
                            "title": "Voir mes demandes",
                            "payload": "/voir_demandes",
                        },
                        {"title": "Aide", "payload": "/demander_aide"},
                    ],
                )
            else:
                dispatcher.utter_message(
                    text="Desole, une erreur est survenue lors de la recherche.",
                    buttons=[
                        {"title": "Reessayer", "payload": "/chercher_reference"},
                        {"title": "Aide", "payload": "/demander_aide"},
                    ],
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Le serveur est temporairement indisponible. Veuillez reessayer.",
                buttons=[
                    {"title": "Contact", "payload": "/contact"},
                    {"title": "Aide", "payload": "/demander_aide"},
                ],
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"Une erreur est survenue : {str(e)}",
                buttons=[{"title": "Aide", "payload": "/demander_aide"}],
            )

        return [SlotSet("reference", reference)]

    def _format_status(self, status: str) -> str:
        status_map = {
            "SOUMISE": "Soumise",
            "EN_TRAITEMENT": "En traitement",
            "VALIDEE": "Validee",
            "REJETEE": "Rejetee",
        }
        return status_map.get(status, status)
