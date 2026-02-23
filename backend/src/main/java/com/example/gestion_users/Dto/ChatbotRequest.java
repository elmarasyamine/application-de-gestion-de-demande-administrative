package com.example.gestion_users.Dto;

public class ChatbotRequest {

    private String message;
    private Long userId;

    public ChatbotRequest() {
    }

    public ChatbotRequest(String message, Long userId) {
        this.message = message;
        this.userId = userId;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }
}
