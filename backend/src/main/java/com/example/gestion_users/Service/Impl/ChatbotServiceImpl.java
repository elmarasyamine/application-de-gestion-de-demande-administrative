package com.example.gestion_users.Service.Impl;

import com.example.gestion_users.Dto.ChatbotResponse;
import com.example.gestion_users.Service.facade.ChatbotService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

/**
 * Service Chatbot qui communique avec le serveur Rasa.
 * Rasa gère la compréhension du langage naturel (NLU) et le dialogue.
 * Les actions custom de Rasa rappellent l'API Spring Boot pour les données.
 */
@Service
public class ChatbotServiceImpl implements ChatbotService {

    @Value("${rasa.server.url:http://localhost:5005}")
    private String rasaServerUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @Override
    public ChatbotResponse processMessage(String message, Long userId) {
        if (message == null || message.trim().isEmpty()) {
            return defaultResponse();
        }

        try {
            // Construire la requête pour Rasa
            Map<String, Object> rasaRequest = new HashMap<>();
            rasaRequest.put("sender", userId != null ? userId.toString() : "anonymous");
            rasaRequest.put("message", message);

            // Ajouter les métadonnées (userId pour les actions custom)
            Map<String, Object> metadata = new HashMap<>();
            metadata.put("userId", userId);
            rasaRequest.put("metadata", metadata);

            // Appeler le serveur Rasa
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(rasaRequest, headers);

            ResponseEntity<List> response = restTemplate.exchange(
                    rasaServerUrl + "/webhooks/rest/webhook",
                    HttpMethod.POST,
                    entity,
                    List.class
            );

            // Traiter la réponse de Rasa
            if (response.getBody() != null && !response.getBody().isEmpty()) {
                return parseRasaResponse(response.getBody());
            }

            return defaultResponse();

        } catch (Exception e) {
            // Si Rasa n'est pas disponible, utiliser le fallback local
            System.err.println("Rasa non disponible, utilisation du fallback local: " + e.getMessage());
            return fallbackResponse(message, userId);
        }
    }

    /**
     * Parse la réponse de Rasa et la convertit en ChatbotResponse
     */
    @SuppressWarnings("unchecked")
    private ChatbotResponse parseRasaResponse(List<Object> rasaMessages) {
        StringBuilder fullText = new StringBuilder();
        List<String> suggestions = new ArrayList<>();

        for (Object msg : rasaMessages) {
            if (msg instanceof Map) {
                Map<String, Object> rasaMsg = (Map<String, Object>) msg;

                // Texte du message
                String text = (String) rasaMsg.get("text");
                if (text != null) {
                    if (fullText.length() > 0) {
                        fullText.append("\n\n");
                    }
                    fullText.append(text);
                }

                // Boutons/Suggestions
                List<Map<String, String>> buttons = (List<Map<String, String>>) rasaMsg.get("buttons");
                if (buttons != null) {
                    for (Map<String, String> button : buttons) {
                        String title = button.get("title");
                        if (title != null) {
                            // Supprimer les emojis en début de titre pour les suggestions
                            String cleanTitle = title.replaceAll("^[\\p{So}\\p{Sk}]+ *", "");
                            suggestions.add(cleanTitle);
                        }
                    }
                }
            }
        }

        if (fullText.length() == 0) {
            return defaultResponse();
        }

        return new ChatbotResponse(fullText.toString(), suggestions);
    }

    /**
     * Réponse de fallback si Rasa n'est pas disponible.
     * Garde une logique basique pour ne pas bloquer l'utilisateur.
     */
    private ChatbotResponse fallbackResponse(String message, Long userId) {
        String msg = message.toLowerCase().trim();

        if (containsAny(msg, "bonjour", "salut", "hello", "hi", "bonsoir", "hey", "salam")) {
            return new ChatbotResponse(
                    "Bonjour ! Je suis l'assistant virtuel.\n\n⚠️ Le service intelligent est temporairement indisponible. Veuillez utiliser les boutons ci-dessous.",
                    Arrays.asList("Voir mes demandes", "Soumettre une demande", "Types de demandes", "Aide"));
        }

        return new ChatbotResponse(
                "⚠️ Le service d'assistant intelligent est temporairement indisponible.\n\n"
                        + "Veuillez utiliser les menus de la plateforme ou réessayer plus tard.",
                Arrays.asList("Voir mes demandes", "Soumettre une demande", "Types de demandes", "Contact", "Aide"));
    }

    private ChatbotResponse defaultResponse() {
        return new ChatbotResponse(
                "Je n'ai pas bien compris votre question.\n\n"
                        + "Essayez l'une de ces options, ou tapez une référence de demande (ex: REF-12345) :",
                Arrays.asList(
                        "Voir mes demandes",
                        "Soumettre une demande",
                        "Types de demandes",
                        "Délais de traitement",
                        "Contact",
                        "Aide"));
    }

    private boolean containsAny(String text, String... keywords) {
        for (String keyword : keywords) {
            if (text.contains(keyword)) {
                return true;
            }
        }
        return false;
    }
}
