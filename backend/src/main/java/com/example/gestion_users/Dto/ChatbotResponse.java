package com.example.gestion_users.Dto;

import java.util.List;

public class ChatbotResponse {

    private String response;
    private List<String> suggestions;

    public ChatbotResponse() {
    }

    public ChatbotResponse(String response, List<String> suggestions) {
        this.response = response;
        this.suggestions = suggestions;
    }

    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        this.response = response;
    }

    public List<String> getSuggestions() {
        return suggestions;
    }

    public void setSuggestions(List<String> suggestions) {
        this.suggestions = suggestions;
    }
}
